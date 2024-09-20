from flask import Flask
from flask import Response
from flask import request
from flask import json
from flask import g
from flask import jsonify, make_response
from tablestore import *
from tablestore.error import *
import random
import subprocess
import os
import json
import sys
import time
import traceback
import urllib.request
import socket
import threading

OTS_ENDPOINT = os.getenv("OTS_ENDPOINT", "https://fc-sched.cn-beijing.ots.aliyuncs.com")
OTS_INSTANCE = os.getenv("OTS_INSTANCE_NAME", "fc-sched")
OTS_TABLENAME = os.getenv("OTS_TABLE_NAME", "endpoints")
OTS_PK = "endpoint"
OTS_REF_KEY = "ref"
OTS_LAST_UPDATE_TMS_KEY = "last_update_tms"
OTS_KEEPALIVE_INTERVAL = 10
REQUEST_ID_HEADER = 'x-fc-request-id'
REQUEST_AK_ID_HEADER = 'x-fc-access-key-id'
REQUEST_AK_SK_HEADER = 'x-fc-access-key-secret'
REQUEST_STS_TOKEN_HEADER = 'x-fc-security-token'
RETRY_SLEEP_SEC = 0.5
RETRY_MAX_TIMES = 10
custom_state = None

app = Flask(__name__)

@app.route('/initialize', methods=['POST'])
def initialize():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Initialize Start RequestId: " + rid)

    # assign backend endpoint
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 

    endpoint = setup(ots_client)
    if endpoint == None or endpoint == "":
        errmsg = { 'Code': 500, 
                    'Message': "fail to reserve the bakcend endpoint.",
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    # start keepalive in background
    period_update_ots_time(ots_client, endpoint)

    print("FC Initialize End RequestId: " + rid)
    return "OK"

def setup(ots_client):
    endpoint = get_available_endpoint(ots_client)
    if endpoint is None or endpoint == "":
        print("[Critical] fail to reserved the backend endpoint")
        return None

    # available to all requests in the entire lifecycle
    global custom_state
    custom_state = {"endpoint" : endpoint}

    print("initialize to reserve backend endpoint: " + endpoint)
    return endpoint

@app.route('/pre-stop', methods=['GET'])
def pre_stop():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Pre-Stop Start RequestId: " + rid)
    
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    
    cleanup(ots_client)
    
    print("FC Pre-Stop End RequestId: " + rid)
    return "OK"

def cleanup(ots_client):
    global custom_state
    if custom_state is None or custom_state["endpoint"] is None or custom_state["endpoint"] == "":
        print("cleanup : no need to release backend endpoint")
        return

    endpoint = custom_state["endpoint"]
    print("cleanup backend endpoint: ", endpoint)
    
    ok = release_endpoint(ots_client, endpoint)
    if ok == False:
        print("[Critical] fail to release the backend endpoint " + endpoint)
    else:
        print("cleanup endpoint:" + endpoint + " succ: ", ok)

    custom_state = None

#@app.teardown_request
#def cleanup_request(exception=None):
#    print("cleanup_request: enter")
#    cleanup()
#    print("cleanup_request: leave")

@app.route('/<path:subpath>', methods=['POST'])
def handler(subpath):
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    # fetch backend srv endpoint
    global custom_state
    if custom_state is None or custom_state["endpoint"] is None or custom_state["endpoint"] == "":
        print("[Critical] unable to process request, since missing neceessary context data(backend_endpoint)")
        errmsg = { 'Code': 500, 
                    'Message': "unable to process request, since missing neceessary context data(backend_endpoint)",
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    endpoint = custom_state["endpoint"]

    # proxy request
    response, err = proxy_request(endpoint, subpath)
    if response:
        response_body = response.read()
        user_rsp = Response(response_body)
        user_rsp.status_code = response.code
        for header, value in response.headers.items():
            print("response header: " + header + ": " + value)
            user_rsp.headers[header] = value
        return user_rsp
    else:
        return {'Code': 500,
                'Message': str(err),
                'Data': "",
                "Success": False
                }, 500, [("Content-Type", "application/json")]

    print("FC Invoke End RequestId: " + rid)

@app.route('/test/proxy_request', methods=['POST'])
def test_proxy_request():
    # mock server
    #     endpoint: 11.238.116.100 
    data = proxy_request("42.81.21.165")
    if data is None:
        return "fail to proxy"
    return data

def proxy_request(endpoint, subpath):
    try:
        url = "http://" + endpoint + "/" + subpath
        method = request.method
        headers = {}
        for header, value in request.headers.items():
            # When forwarding a request, remove the X-Fc request header to avoid leaking sensitive information.
            if header.startswith("X-Fc") == False:
                headers[header] = value
        data = request.data
        timeout = 600
        print("proxy_request url:", url)
        print("proxy_request method:", method)
        print("proxy_request headers:", headers)
        print("proxy_request data:", data)
        print("proxy_request timeout:", timeout)

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        response = urllib.request.urlopen(req, timeout=timeout)
        return response, None

    except urllib.error.HTTPError as e:
        print("proxy_request failed, HTTP Error:", e)
        return None, e
    except urllib.error.URLError as e:
        print("proxy_request failed, URL Error:", e)
        return None, e
    except Exception as e:
        print("proxy_request failed, Exception Error:", e)
        return None, e

@app.route('/test/get_available_endpoint', methods=['POST'])
def test_get_available_endpoint():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    endpoint = get_available_endpoint(ots_client)
    return endpoint or "Never reach here"

def get_available_endpoint(ots_client):
    # blocking until:
    #     1. get available endpoint ok
    #     2. function timeout
    while True:
        all_available_endpoints = get_all_available_endpoints(ots_client)
        if len(all_available_endpoints) == 0:
            time.sleep(RETRY_SLEEP_SEC)
            continue

        random.shuffle(all_available_endpoints)
        for endpoint in all_available_endpoints:
            ok = update_ots_ref(ots_client, endpoint, 1, True)
            if ok == True:
                return endpoint
        time.sleep(RETRY_SLEEP_SEC)

@app.route('/test/release_endpoint', methods=['POST'])
def test_release_endpoint():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    ok = release_endpoint(ots_client, "1.2.3.4")
    return "release_endpoint : %s" % ok

def release_endpoint(ots_client, endpoint):
    for _ in range(RETRY_MAX_TIMES):
        ok = update_ots_ref(ots_client, endpoint, 0, False)
        if ok == True:
            return True
        time.sleep(RETRY_SLEEP_SEC)

    return False

@app.route('/test/update_ots_ref', methods=['POST'])
def test_update_ots_ref():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    #ok = update_ots_ref(ots_client, "1.2.3.4", 1, True)
    ok = update_ots_ref(ots_client, "1.2.3.4", 0, False)
    return "update succ : %s" % ok

def update_ots_ref(client, endpoint, ref, cnd_sw):
    try:
        primary_key = [(OTS_PK, endpoint)]
        update_of_attribute_columns = {
            'PUT': [(OTS_REF_KEY, ref)],
        }
        row = Row(primary_key, update_of_attribute_columns)
        if cnd_sw == True:
            condition = Condition(RowExistenceExpectation.EXPECT_EXIST, SingleColumnCondition(OTS_REF_KEY, 1-ref, ComparatorType.EQUAL))
            client.update_row(OTS_TABLENAME, row, condition)
        else:
            condition = Condition(RowExistenceExpectation.EXPECT_EXIST)
            client.update_row(OTS_TABLENAME, row, condition)

        return True
    except OTSClientError as e:
        print('update_ots_ref failed, OTSClientError info:', e)
    except OTSServiceError as e:
        print('update_ots_ref failed, OTSServiceError info:', e)
    except Exception as e:
        print('update_ots_ref failed, Exception info:', e)

    return False

def update_ots_time(client, endpoint):
    cond_check_fail = False
    try:
        primary_key = [(OTS_PK, endpoint)]
        update_of_attribute_columns = {
            'PUT': [(OTS_LAST_UPDATE_TMS_KEY, int(time.time()))],
        }
        row = Row(primary_key, update_of_attribute_columns)
        condition = Condition(RowExistenceExpectation.EXPECT_EXIST, SingleColumnCondition(OTS_REF_KEY, 1, ComparatorType.EQUAL))
        client.update_row(OTS_TABLENAME, row, condition)

        return True, cond_check_fail
    except OTSClientError as e:
        print('update_ots_time failed, OTSClientError info:', e)
    except OTSServiceError as e:
        cond_check_fail = True
        print('update_ots_time failed, OTSServiceError info:', e)
    except Exception as e:
        print('update_ots_time failed, Exception info:', e)

    return False, cond_check_fail

def period_update_ots_time(client, endpoint):
    print("forwarding backend endpoint is: ", endpoint)
    rv, cond_check_fail = update_ots_time(client, endpoint)
    if rv == False:
        print("[Critical] update_ots_time failed.")

        # When downsizing occurs, the change in the relationship between CPU instances and GPU instances 
        # may cause periodic update time failure (conditional failure), requiring the container instance
        # to obtain the backend GPU IP address again.
        if cond_check_fail == True:
            new_endpoint = setup(client)
            if new_endpoint != None and new_endpoint != "":
                print("[Notice] change backend endpoint from %s to %s" % (endpoint, new_endpoint))
                endpoint = new_endpoint
    threading.Timer(OTS_KEEPALIVE_INTERVAL, period_update_ots_time, [client, endpoint]).start()

@app.route('/test/get_all_available_endpoints', methods=['POST'])
def test_get_all_available_endpoints():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    endpoints = get_all_available_endpoints(ots_client)
    print("endpoints:", endpoints)
    return endpoints

def get_all_available_endpoints(client):
    inclusive_start_primary_key = [(OTS_PK, INF_MIN)]
    exclusive_end_primary_key = [(OTS_PK, INF_MAX)]
    limit = 5000
    cond = SingleColumnCondition(OTS_REF_KEY, 0, ComparatorType.EQUAL, pass_if_missing=False)
    output = []

    try:
        consumed, next_start_primary_key, row_list, next_token = client.get_range(
            OTS_TABLENAME, Direction.FORWARD,
            inclusive_start_primary_key, exclusive_end_primary_key,
            limit = limit,
            column_filter=cond)

        all_rows = []
        all_rows.extend(row_list)

        while next_start_primary_key is not None:
            inclusive_start_primary_key = next_start_primary_key
            consumed, next_start_primary_key, row_list, next_token = client.get_range(
                OTS_TABLENAME, Direction.FORWARD,
                inclusive_start_primary_key, exclusive_end_primary_key,
                limit = limit,
                column_filter=cond)
            all_rows.extend(row_list)

        for row in all_rows:
            #eg: [('endpoint', '11.22.33.55')] [('ref', 0, 1713529197733)]
            print(row.primary_key, row.attribute_columns)
            output.append(row.primary_key[0][1])
        print("fetch endpoints result: ", output)
    except OTSClientError as e:
        print('get_all_available_endpoints failed, OTSClientError info:', e)
    except OTSServiceError as e:
        print('get_all_available_endpoints failed, OTSServiceError info:', e)
    except Exception as e:
        print('get_all_available_endpoints failed, Exception info:', e)

    return output

def fetch_ctx_info():
    ak_id = request.headers.get(REQUEST_AK_ID_HEADER)
    ak_sk = request.headers.get(REQUEST_AK_SK_HEADER)
    sts_token = request.headers.get(REQUEST_STS_TOKEN_HEADER)
    return ak_id, ak_sk, sts_token

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
