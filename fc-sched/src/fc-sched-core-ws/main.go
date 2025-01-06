package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"

	"github.com/gorilla/mux"
	"github.com/gorilla/websocket"

	endpoint "ws-proxy/endpoint"
)

const (
	REQUEST_ID_HEADER        = "x-fc-request-id"
	REQUEST_AK_ID_HEADER     = "x-fc-access-key-id"
	REQUEST_AK_SK_HEADER     = "x-fc-access-key-secret"
	REQUEST_STS_TOKEN_HEADER = "x-fc-security-token"
)

// WebSocket upgrader
var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

var (
	OTS_ENDPOINT  = getEnv("OTS_ENDPOINT", "https://fc-sched.cn-beijing.ots.aliyuncs.com")
	OTS_INSTANCE  = getEnv("OTS_INSTANCE_NAME", "fc-sched")
	OTS_TABLENAME = getEnv("OTS_TABLE_NAME", "endpoints")

	endpointClient *endpoint.Endpoint
	once           sync.Once
)

func main() {
	r := mux.NewRouter()

	r.PathPrefix("/initialize").HandlerFunc(handleInitialize).Methods("POST")
	r.PathPrefix("/pre-stop").HandlerFunc(handlePreStop).Methods("GET")
	r.PathPrefix("/{path}/{subpath}").HandlerFunc(handleWebSocket)

	log.Println("Starting server on :9000")
	if err := http.ListenAndServe("0.0.0.0:9000", r); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	path := vars["path"]
	subpath := vars["subpath"]
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Failed to upgrade connection: %v", err)
		return
	}
	defer conn.Close()

	log.Printf("path: %v subpath: %v\n", path, subpath)

	downstreamServer := fmt.Sprintf("ws://%s/%s/%s", endpointClient.GetEndpoint(), path, subpath)

	log.Printf("downstream url path is %v\n", downstreamServer)

	downstreamConn, _, err := websocket.DefaultDialer.Dial(downstreamServer, nil)
	if err != nil {
		log.Printf("Failed to connect to downstream server: %v", err)
		return
	}
	log.Printf("connected downstream ecs")
	defer downstreamConn.Close()

	done := make(chan struct{})

	go forwardMessages(conn, downstreamConn, done)
	go forwardMessages(downstreamConn, conn, done)

	<-done
}

func forwardMessages(src, dst *websocket.Conn, done chan struct{}) {
	for {
		messageType, message, err := src.ReadMessage()
		if err != nil {
			log.Printf("Error reading message: %v", err)
			once.Do(func() {
				close(done)
			})
			break
		}

		err = dst.WriteMessage(messageType, message)
		if err != nil {
			log.Printf("Error writing message: %v", err)
			once.Do(func() {
				close(done)
			})
			break
		}
		log.Printf("Received message and forwarded: %s", string(message))
	}
}

func handleInitialize(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}
	log.Println(r.Header)

	requestId := r.Header.Get(REQUEST_ID_HEADER)
	log.Printf("FC Initialize Start RequestId: %v\n", requestId)

	akId, akSk, stsToken := fetchCtxInfo(r)
	endpointClient = endpoint.NewClient(OTS_ENDPOINT, OTS_INSTANCE, OTS_TABLENAME, akId, akSk, stsToken)

	w.Header().Set("Content-Type", "application/json")

	endpoint, err := endpointClient.Setup()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"Code":    500,
			"Message": "failed to reserve the backend endpoint",
			"Success": false,
		})
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]interface{}{
		"Code":    200,
		"message": "reserve the backend endpoint",
		"Success": true,
	})
	log.Printf("reserve the banckend endpoint %v successfully", endpoint)
	log.Printf("FC Initialize End RequestId: %v\n", requestId)
	return
}

func handlePreStop(w http.ResponseWriter, r *http.Request) {
	rid := r.Header.Get(REQUEST_ID_HEADER)
	log.Printf("FC Pre-Stop Start RequestId: %v\n", rid)

	if endpointClient == nil {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"Code":    500,
			"message": "failed to cleanup the backend endpoint due to nil endpoint client",
			"Success": false,
		})
	}

	endpointClient.Cleanup()

	print("FC Pre-Stop End RequestId: " + rid)
	json.NewEncoder(w).Encode(map[string]interface{}{
		"Code":    200,
		"message": "cleanup the backend endpoint",
		"Success": true,
	})
}

func fetchCtxInfo(r *http.Request) (akId, akSk, stsToken string) {
	return r.Header.Get(REQUEST_AK_ID_HEADER), r.Header.Get(REQUEST_AK_SK_HEADER), r.Header.Get(REQUEST_STS_TOKEN_HEADER)
}

func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}
