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


OTS_ENDPOINT = os.getenv("OTS_ENDPOINT", "https://fc-sched.cn-beijing.ots.aliyuncs.com")
OTS_INSTANCE = os.getenv("OTS_INSTANCE_NAME", "fc-sched")
OTS_TABLENAME = os.getenv("OTS_TABLE_NAME","endpoints")
REQUEST_ID_HEADER = 'x-fc-request-id'
REQUEST_AK_ID_HEADER = 'x-fc-access-key-id'
REQUEST_AK_SK_HEADER = 'x-fc-access-key-secret'
REQUEST_STS_TOKEN_HEADER = 'x-fc-security-token'
OTS_PK = "endpoint"
OTS_REF_KEY = "ref"
RETRY_SLEEP_SEC = 0.2
RETRY_MAX_TIMES = 60
custom_state = None


app = Flask(__name__)


@app.route('/initialize', methods=['POST'])
def initialize():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Initialize Start RequestId: " + rid)

    # assign backend endpoint
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    ip = get_available_ip(ots_client)
    if ip is None or ip == "":
        print("[Critical] fail to reserved the backend ip")
        errmsg = { 'Code': 500, 
                    'Message': str("fail to reserve the bakcend ip."),
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    # available to all requests in the entire lifecycle
    global custom_state
    custom_state = {"ip" : ip}
    print("initialize to reserve backend ip: " + ip)

    print("FC Initialize End RequestId: " + rid)
    return "OK"


@app.route('/pre-stop', methods=['GET'])
def pre_stop():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Pre-Stop Start RequestId: " + rid)
    cleanup()
    print("FC Pre-Stop End RequestId: " + rid)
    return "OK"

def cleanup():
    global custom_state
    if custom_state is None or custom_state["ip"] is None or custom_state["ip"] == "":
        print("cleanup : no need to release backend ip")
        return

    ip = custom_state["ip"]
    print("cleanup ip: ", ip)
    
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    ok = release_ip(ots_client, ip)
    if ok == False:
        print("[Critical] fail to release the backend ip " + ip)
    else:
        print("cleanup ip:" + ip + " succ: ", ok)

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

    # fetch backend srv ip
    global custom_state
    if custom_state is None or custom_state["ip"] is None or custom_state["ip"] == "":
        print("[Critical] unable to process request, since missing neceessary context data(backend_ip)")
        errmsg = { 'Code': 500, 
                    'Message': str("unable to process request, since missing neceessary context data(backend_ip)"),
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    ip = custom_state["ip"]

    response, err = proxy_request(ip, subpath)
    if response:
        response_body = response.read()
        user_rsp = Response(response_body)
        user_rsp.status_code = response.code
        for header, value in response.headers.items():
            print("handler user_rsp: " + header + ": " + value)
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
    #     ip: 11.238.116.100 
    data = proxy_request("42.81.21.165")
    if data is None:
        return "fail to proxy"
    return data

def proxy_request(ip, subpath):
    try:
        url = "http://" + ip + ":7860/" + subpath
        #headers = {
        #    "Content-Type": request.headers.get('Content-Type'),
        #    "X-Model-Best-Model": request.headers.get('X-Model-Best-Model'),
        #}
        headers = request.headers
        data = request.data
        timeout = 600
        print("proxy_request url:", url)
        print("proxy_request headers:", headers)
        print("proxy_request data:", data)
        print("proxy_request timeout:", timeout)

        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
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


#def proxy_request(ip):
#    # TODO:
#    #     if the response body is very large, change to streaming here
#    #     improve later.
#    try:
#        inference_url = ip + ":5000/generate_aud"
#        #inference_url = "http://" + ip + ":80/"
#        x_model_best_model = request.headers.get('X-Model-Best-Model')
#        content_type = request.headers.get('Content-Type')
#        data = request.data
#        print("proxy_request inference_url:", inference_url)
#        print("proxy_request x_model_best_model:", x_model_best_model)
#        print("proxy_request content_type:", content_type)
#        print("proxy_request data:", data)
#
#        cmd = ['curl', '-X', 'POST', inference_url, '-H', f'X-Model-Best-Model: {x_model_best_model}', '-H', f'Content-Type: {content_type}', '-d', data]
#        #cmd = ['curl', inference_url, '-H', 'Host: www.sina.com.cn']
#        print("proxy_request command:", cmd)
#
#        result = subprocess.run(cmd, capture_output=True, text=True)
#        print(result.stdout)
#        return result.stdout
#    except Exception as e:
#        print('proxy_request failed, Exception info:', e)
#
#    return None


@app.route('/test/get_available_ip', methods=['POST'])
def test_get_available_ip():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    ip = get_available_ip(ots_client)
    return ip or "Never reach here"

def get_available_ip(ots_client):
    # blocking until:
    #     1. get available ip ok
    #     2. function timeout
    while True:
        all_available_endpoints = get_all_available_endpoints(ots_client)
        if len(all_available_endpoints) == 0:
            time.sleep(RETRY_SLEEP_SEC)
            continue

        random.shuffle(all_available_endpoints)
        for ip in all_available_endpoints:
            ok = update_ots_row(ots_client, ip, 1, True)
            if ok == True:
                return ip
        time.sleep(RETRY_SLEEP_SEC)


@app.route('/test/release_ip', methods=['POST'])
def test_release_ip():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    ok = release_ip(ots_client, "1.2.3.4")
    return "release_ip : %s" % ok

def release_ip(ots_client, ip):
    # TODO: 
    #     if release_ip fails, there will be dirty data
    #     fix later.
    for _ in range(RETRY_MAX_TIMES):
        ok = update_ots_row(ots_client, ip, 0, False)
        if ok == True:
            return True
        time.sleep(RETRY_SLEEP_SEC)

    return False


@app.route('/test/update_ots_row', methods=['POST'])
def test_update_ots_row():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    #ok = update_ots_row(ots_client, "1.2.3.4", 1, True)
    ok = update_ots_row(ots_client, "1.2.3.4", 0, False)
    return "update succ : %s" % ok

def update_ots_row(client, endpoint, ref, cnd_sw):
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
        print('update_ots_row failed, OTSClientError info:', e)
    except OTSServiceError as e:
        # if condition fail, hit OTSServiceError
        # update_ots_row failed, OTSServiceError info: ErrorCode: OTSConditionCheckFail, ErrorMessage: Condition check failed.
        print('update_ots_row failed, OTSServiceError info:', e)
    except Exception as e:
        print('update_ots_row failed, Exception info:', e)

    return False


@app.route('/test/get_all_available_endpoints', methods=['POST'])
def test_get_all_available_endpoints():
    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    ips = get_all_available_endpoints(ots_client)
    print("ips:", ips)
    return ips

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
        print('Total rows: ', len(all_rows))
        print("output: ", output)
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
