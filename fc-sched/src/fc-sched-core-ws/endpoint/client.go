package Endpoint

import (
	"log"
	"math/rand"
	"time"

	"github.com/aliyun/aliyun-tablestore-go-sdk/tablestore"
)

const (
	OTS_PK                  = "endpoint"
	OTS_REF_KEY             = "ref"
	OTS_LAST_UPDATE_TMS_KEY = "last_update_tms"
	OTS_KEEPALIVE_INTERVAL  = 10
	RETRY_SLEEP_MS          = 500
	RETRY_MAX_TIMES         = 10
)

type Endpoint struct {
	client    *tablestore.TableStoreClient
	endpoint  string
	tableName string
	done      chan struct{}
}

func NewClient(endpoint string, otsInstance, tableName, accessKeyId, accessKeySecret, stsToken string) *Endpoint {
	config := tablestore.NewDefaultTableStoreConfig()
	return &Endpoint{
		client:    tablestore.NewClientWithConfig(endpoint, otsInstance, accessKeyId, accessKeySecret, stsToken, config),
		endpoint:  "",
		tableName: tableName,
		done:      make(chan struct{}),
	}
}

func (c *Endpoint) Setup() (string, error) {
	endpoint, err := c.getAvailableEndpoint()
	if err != nil || endpoint == "" {
		log.Printf("[Critical] failed to reserved the backend endpoint")
		return "", err
	}
	c.endpoint = endpoint

	go func() {
		otsTimestampUpdateTicker := time.NewTicker(OTS_KEEPALIVE_INTERVAL * time.Second)
		for {
			select {
			case <-otsTimestampUpdateTicker.C:
				c.updateOTSTimestampPeriodically()
			case <-c.done:
				log.Printf("stop periodically update OTS timestamp\n")
				return
			}
		}
	}()

	log.Printf("initialize to reserve backend endpoint: %v", c.endpoint)
	return endpoint, nil
}

func (c *Endpoint) Cleanup() error {
	// stop update OTS timstamp first
	close(c.done)

	endpoint := c.endpoint
	if endpoint == "" {
		log.Printf("cleanup: no need to release backend endpoint\n")
		return nil
	}
	log.Printf("cleanup: backend endpoint: %v\n", endpoint)
	err := c.releaseEndpoint(endpoint)
	if err != nil {
		log.Printf("[Critical] fail to release the backend endpoint %v\n", endpoint)
		return err
	}
	log.Printf("clean up backend endpoint %v successfully\n", endpoint)
	c.endpoint = ""
	return nil
}

func (c *Endpoint) GetEndpoint() string {
	return c.endpoint
}

func (c *Endpoint) getAvailableEndpoint() (string, error) {
	for {
		endpoints, err := c.getAllAvailableEndpoints()
		if err != nil {
			log.Printf("get all available endpoints failed due to %v", err)
			time.Sleep(RETRY_SLEEP_MS * time.Millisecond)
			continue
		}
		// shuffle endpoints
		shuffleSlice(endpoints)
		for _, endpoint := range endpoints {
			err = c.updateOTSRef(endpoint, 1, true)
			if err != nil {
				log.Printf("updateOTSRef failed due to %v", err)
				time.Sleep(RETRY_SLEEP_MS * time.Millisecond)
				continue
			}
			log.Printf("updateOTSRef %v", endpoint)
			return endpoint, nil
		}
		time.Sleep(RETRY_SLEEP_MS * time.Millisecond)
	}
}

func (c *Endpoint) getAllAvailableEndpoints() ([]string, error) {
	var output []string

	startPK := new(tablestore.PrimaryKey)
	startPK.AddPrimaryKeyColumnWithMinValue(OTS_PK)
	endPK := new(tablestore.PrimaryKey)
	endPK.AddPrimaryKeyColumnWithMaxValue(OTS_PK)

	// set query condition
	cond := tablestore.NewSingleColumnCondition(OTS_REF_KEY, tablestore.CT_EQUAL, int64(0))

	rangeRowQueryCriteria := &tablestore.RangeRowQueryCriteria{
		TableName:       c.tableName,
		StartPrimaryKey: startPK,
		EndPrimaryKey:   endPK,
		Direction:       tablestore.FORWARD,
		MaxVersion:      1,
		Limit:           5000,
		Filter:          cond,
	}

	getRangeReq := &tablestore.GetRangeRequest{
		RangeRowQueryCriteria: rangeRowQueryCriteria,
	}

	getRangeResp, err := c.client.GetRange(getRangeReq)
	if err != nil {
		log.Printf("get range failed due to %v", err)
		return output, err
	}
	log.Printf("get range result is %+v", getRangeResp.Rows)

	for {
		if err != nil {
			log.Printf("get range failed with err: %v", err)
		}
		for _, row := range getRangeResp.Rows {
			log.Printf("row primary key %v, attribute columns %+v",
				row.PrimaryKey, row.Columns)
			output = append(output, row.PrimaryKey.PrimaryKeys[0].Value.(string))
		}
		if getRangeResp.NextStartPrimaryKey == nil {
			log.Println("nex start primary key is nil")
			break
		} else {
			log.Printf("next pk is: %+v", getRangeResp.NextStartPrimaryKey)
			getRangeReq.RangeRowQueryCriteria.StartPrimaryKey = getRangeResp.NextStartPrimaryKey
			getRangeResp, err = c.client.GetRange(getRangeReq)
		}
	}
	return output, nil
}

func (c *Endpoint) updateOTSRef(endpoint string, ref int64, condition bool) error {
	// prepare updatePK
	updatePK := new(tablestore.PrimaryKey)
	updatePK.AddPrimaryKeyColumn(OTS_PK, endpoint)

	// prepare updateRowChange
	updateRowChange := new(tablestore.UpdateRowChange)
	updateRowChange.TableName = c.tableName
	updateRowChange.PrimaryKey = updatePK
	updateRowChange.PutColumn(OTS_REF_KEY, ref)
	updateRowChange.SetCondition(tablestore.RowExistenceExpectation_EXPECT_EXIST)
	if condition {
		updateRowChange.SetColumnCondition(tablestore.NewSingleColumnCondition(OTS_REF_KEY, tablestore.CT_EQUAL, 1-ref))
	}

	// prepare updateRowRequest
	updateRowReq := &tablestore.UpdateRowRequest{
		UpdateRowChange: updateRowChange,
	}
	_, err := c.client.UpdateRow(updateRowReq)
	if err != nil {
		log.Printf("updateOTSRef failed due to %v\n", err)
		return err
	}
	return nil
}

func (c *Endpoint) updateOTSTimestamp(endpoint string) (bool, error) {
	// prepare updatePK
	updatePK := new(tablestore.PrimaryKey)
	updatePK.AddPrimaryKeyColumn(OTS_PK, endpoint)

	// prepare updateRowChange
	updateRowChange := new(tablestore.UpdateRowChange)
	updateRowChange.TableName = c.tableName
	updateRowChange.PrimaryKey = updatePK
	updateRowChange.PutColumn(OTS_LAST_UPDATE_TMS_KEY, time.Now().UnixMilli())
	updateRowChange.SetCondition(tablestore.RowExistenceExpectation_EXPECT_EXIST)
	updateRowChange.SetColumnCondition(tablestore.NewSingleColumnCondition(OTS_REF_KEY, tablestore.CT_EQUAL, int64(1)))

	// prepare updateRowRequest
	updateRowReq := &tablestore.UpdateRowRequest{
		UpdateRowChange: updateRowChange,
	}
	_, err := c.client.UpdateRow(updateRowReq)
	if err != nil {
		log.Printf("updateOTSRef failed due to %v\n", err)
		return false, err
	}
	return true, nil
}

func (c *Endpoint) updateOTSTimestampPeriodically() {
	endpoint := c.endpoint
	log.Printf("forwarding backend endpoint is %v", endpoint)
	rc, err := c.updateOTSTimestamp(endpoint)
	if !rc {
		log.Printf("[Critical] updateOTSTimestamp failed.")
		if err != nil {
			newEndpoint, err := c.Setup()
			if err != nil || newEndpoint == "" {
				log.Printf("[Notice] change backend endpoint from %v to %v\n", endpoint, newEndpoint)
				c.endpoint = endpoint
			}
		}
	}
}

func (c *Endpoint) releaseEndpoint(endpoint string) error {
	for i := 0; i < RETRY_MAX_TIMES; i++ {
		err := c.updateOTSRef(endpoint, 0, false)
		if err != nil {
			log.Printf("releaseEndpoint failed due to %v", err)
			time.Sleep(RETRY_SLEEP_MS * time.Millisecond)
			continue
		}
		return nil
	}
	return nil
}

func shuffleSlice(slice []string) {
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(slice), func(i, j int) {
		slice[i], slice[j] = slice[j], slice[i]
	})
}
