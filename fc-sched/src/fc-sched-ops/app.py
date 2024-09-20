from alibabacloud_fc20230330.client import Client as FC20230330Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_fc20230330 import models as fc20230330_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from flask import Flask
from flask import request
from flask import json
from flask import jsonify, make_response
from typing import List
from tablestore import *
import time
import json
import os
import threading

OTS_ENDPOINT = os.getenv("OTS_ENDPOINT", "https://fc-sched.cn-beijing.ots.aliyuncs.com")
OTS_INSTANCE = os.getenv("OTS_INSTANCE_NAME", "fc-sched")
OTS_TABLENAME = os.getenv("OTS_TABLE_NAME","endpoints")
OTS_PK = "endpoint"
OTS_REF_KEY = "ref"
OTS_LAST_UPDATE_TMS_KEY = "last_update_tms"
OTS_RECORD_LIVE_TTL = 60
REQUEST_ID_HEADER = 'x-fc-request-id'
REQUEST_AK_ID_HEADER = 'x-fc-access-key-id'
REQUEST_AK_SK_HEADER = 'x-fc-access-key-secret'
REQUEST_STS_TOKEN_HEADER = 'x-fc-security-token'
REQUEST_REGION_HEADER = 'x-fc-region'
REQUEST_FUNCTION_NAME_HEADER = 'x-fc-function-name'
REQUEST_UID = 'x-fc-account-id'

app = Flask(__name__)

@app.route('/initialize', methods=['POST'])
def initialize():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Initialize Start RequestId: " + rid)

    # start keepalive in background
    ak_id, ak_sk, sts_token, _, _, _ = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token)

    period_check_leak_endpoints(ots_client)

    print("FC Initialize End RequestId: " + rid)
    return "OK"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world(path):
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)
    print("FC Invoke End RequestId: " + rid)
    return "Usage: (1). /endpoint/register?ip=x.x.x.x  (2). /endpoint/unregister?ip=y.y.y.y  (3). /endpoint/list"

@app.route('/endpoint/register', methods=['GET'])
def register_endpoint():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    ip = request.args.get("ip")
    if ip is None:
        return "missing necessary argument: ?ip=x.x.x.x"

    # step1: register in database
    ak_id, ak_sk, sts_token, _, _, _ = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token)

    rv = insert_endpoint(ots_client, ip)
    if rv == False:
        errmsg = { 'Code': 500, 
                    'Message': "fail to register the bakcend ip.",
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    # step2: setup concurrency & provision for fc-sched-core
    rv = do_sync_concurrency_and_provision(ots_client, True)
    if rv == False:
        errmsg = { 'Code': 500, 
                    'Message': "fail to auto-adjust the number of forwarding instances.",
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    print("FC Invoke End RequestId: " + rid)
    return "register succ"

def insert_endpoint(ots_client, ip):
    primary_key = [('endpoint', ip)]
    attribute_columns = [('ref', 0)]
    row = Row(primary_key, attribute_columns)
    try:
        consumed, return_row = ots_client.put_row(OTS_TABLENAME, row)
        return True
    except OTSClientError as e:
        print("register endpoint failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print("register endpoint failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))                    
    except Exception as e:
        print("register endpoint failed, error_message:%s" % e.get_error_message())
    return False

@app.route('/endpoint/unregister', methods=['GET'])
def unregister_endpoint():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    ip = request.args.get("ip")
    if ip is None:
        return "missing necessary argument: ?ip=x.x.x.x"

    # step1: unregister in database
    ak_id, ak_sk, sts_token, _, _, _ = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token)

    rv = delete_endpoint(ots_client, ip)
    if rv == False:
        errmsg = { 'Code': 500, 
                    'Message': "fail to unregister the bakcend ip.",
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    # step2: setup concurrency & provision for fc-sched-core
    rv = do_sync_concurrency_and_provision(ots_client, False)
    if rv == False:
        errmsg = { 'Code': 500, 
                    'Message': "fail to auto-adjust the number of forwarding instances.",
                    "Success": False }
        return errmsg, 500, [("Content-Type", "application/json")]

    print("FC Invoke End RequestId: " + rid)
    return "unregister succ"

def delete_endpoint(ots_client, ip):
    primary_key = [('endpoint', ip)]
    row = Row(primary_key)
    try:
        consumed, return_row = ots_client.delete_row(OTS_TABLENAME, row, None)
        return True
    except OTSClientError as e:
        print("unregister endpoint failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print("unregister endpoint failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))
    except Exception as e:
        print("unregister endpoint failed, error_message:%s" % e.get_error_message())
    return False

@app.route('/endpoint/list', methods=['GET'])
def list_endpoint():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    ak_id, ak_sk, sts_token, _, _, _ = fetch_ctx_info()
    ots_client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    output = fetch_endpoints(ots_client)

    print("FC Invoke End RequestId: " + rid)
    return make_response(jsonify(output), 200)

def fetch_endpoints(ots_client):
    inclusive_start_primary_key = [('endpoint', INF_MIN)]
    exclusive_end_primary_key = [('endpoint', INF_MAX)]
    limit = 5000
    output = []
    try:
        consumed, next_start_primary_key, row_list, next_token = ots_client.get_range(
            OTS_TABLENAME, Direction.FORWARD,
            inclusive_start_primary_key, exclusive_end_primary_key,
            limit = limit)

        all_rows = []
        all_rows.extend(row_list)

        while next_start_primary_key is not None:
            inclusive_start_primary_key = next_start_primary_key
            consumed, next_start_primary_key, row_list, next_token = ots_client.get_range(
                OTS_TABLENAME, Direction.FORWARD,
                inclusive_start_primary_key, exclusive_end_primary_key,
                limit = limit)
            all_rows.extend(row_list)

        for row in all_rows:
            #eg: [('endpoint', '11.22.33.55')] [('ref', 0, 1713529197733)]
            #eg: [('endpoint', '47.92.208.112')] [('last_update_tms', 1726739585, 1726739585963), ('ref', 1, 1726717719291)]
            #print(row.primary_key, row.attribute_columns)
            record = {"endpoint" : row.primary_key[0][1]}
            for item in row.attribute_columns:
                if item[0] == "ref":
                    record["ref"] = item[1]
                elif item[0] == "last_update_tms":
                    record["last_update_tms"] = item[1]
            output.append(record)
        print("fetch endpoints result: ", output)
        return output
    except OTSClientError as e:
        print('get row failed, http_status:%d, error_message:%s' % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print('get row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s' % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))
    return []

def reset_endpoint_ref(ots_client, endpoint):
    try:
        primary_key = [(OTS_PK, endpoint)]
        update_of_attribute_columns = {
            'PUT': [(OTS_REF_KEY, 0)],
        }
        row = Row(primary_key, update_of_attribute_columns)
        condition = Condition(RowExistenceExpectation.EXPECT_EXIST)
        ots_client.update_row(OTS_TABLENAME, row, condition)
        return True
    except OTSClientError as e:
        print('update_ots_ref failed, OTSClientError info:', e)
    except OTSServiceError as e:
        print('update_ots_ref failed, OTSServiceError info:', e)
    except Exception as e:
        print('update_ots_ref failed, Exception info:', e)
    return False

def check_leak_endpoints(ots_client):
    endpoints = fetch_endpoints(ots_client)
    leak_endpoints = []
    leak_time = int(time.time()) - OTS_RECORD_LIVE_TTL

    for ep in endpoints:
        if ep["ref"] == None or ep["ref"] == 0:
            continue
        if ep["last_update_tms"] == None or ep["last_update_tms"] == "":
            continue
        if ep["last_update_tms"] < leak_time:
            leak_endpoints.append(ep["endpoint"])
    
    print("check leak endpoint: ", leak_endpoints)
    for ep in leak_endpoints:
        reset_endpoint_ref(ots_client, ep)

def period_check_leak_endpoints(ots_client):
    check_leak_endpoints(ots_client)
    threading.Timer(OTS_RECORD_LIVE_TTL, period_check_leak_endpoints, [ots_client]).start()

def do_sync_concurrency_and_provision(ots_client, inc):
    ak_id, ak_sk, sts_token, region, func_ops_name, uid = fetch_ctx_info()
    fc_client = create_fc_client(region, ak_id, ak_sk, sts_token, uid)
    func_core_name = fetch_core_func_name(func_ops_name)
    n = len(fetch_endpoints(ots_client))
    rv = True

    if inc == True:
        # sync concurrency before provision
        if do_put_concurrency(fc_client, func_core_name, n) == False:
            rv = False
        if do_put_provision(fc_client, func_core_name, n) == False:
            rv = False
    else:
        # sync provision before concurrency
        if do_put_provision(fc_client, func_core_name, n) == False:
            rv = False
        if do_put_concurrency(fc_client, func_core_name, n) == False:
            rv = False

    return rv

def do_put_concurrency(client, func_core_name, n):
    put_concurrency_input = fc20230330_models.PutConcurrencyInput(
        reserved_concurrency = n
    )
    put_concurrency_config_request = fc20230330_models.PutConcurrencyConfigRequest(
        body = put_concurrency_input
    )
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        client.put_concurrency_config_with_options(func_core_name, put_concurrency_config_request, headers, runtime)
        return True
    except Exception as error:
        print(error.message)
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
    return False

def do_put_provision(client, func_core_name, n):
    put_provision_config_input = fc20230330_models.PutProvisionConfigInput(
        always_allocate_cpu = True,
        target = n
    )
    put_provision_config_request = fc20230330_models.PutProvisionConfigRequest(
        body = put_provision_config_input,
        qualifier = 'LATEST'
    )
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        client.put_provision_config_with_options(func_core_name, put_provision_config_request, headers, runtime)
        return True
    except Exception as error:
        print(error.message)
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
    return False

def do_get_function(client, func_core_name):
    get_function_request = fc20230330_models.GetFunctionRequest()
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        return client.get_function_with_options('fc-sched-2235-core', get_function_request, headers, runtime)
    except Exception as error:
        print(error.message)
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
    return None

def do_update_function(client, func_core_name, envs):
    update_function_input_environment_variables = envs
    update_function_input = fc20230330_models.UpdateFunctionInput(
        environment_variables = update_function_input_environment_variables
    )
    update_function_request = fc20230330_models.UpdateFunctionRequest(
        body = update_function_input
    )
    runtime = util_models.RuntimeOptions()
    headers = {}
    try:
        client.update_function_with_options(func_core_name, update_function_request, headers, runtime)
        return True
    except Exception as error:
        print(error.message)
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
    return False

def create_fc_client(region, ak_id, ak_sk, sts_token, uid):
    config = open_api_models.Config(
        access_key_id=ak_id,
        access_key_secret=ak_sk,
        security_token=sts_token,
    )
    config.endpoint = '%s.%s.fc.aliyuncs.com' % (uid, region)
    return FC20230330Client(config)

def fetch_core_func_name(func_ops_name):
    if str.endswith(func_ops_name, "-ops") == True:
        arr = str.split(func_ops_name, "-ops")
        return arr[0] + "-core"
    return ""

def fetch_ctx_info():
    ak_id = request.headers.get(REQUEST_AK_ID_HEADER)
    ak_sk = request.headers.get(REQUEST_AK_SK_HEADER)
    sts_token = request.headers.get(REQUEST_STS_TOKEN_HEADER)
    region = request.headers.get(REQUEST_REGION_HEADER)
    func_name = request.headers.get(REQUEST_FUNCTION_NAME_HEADER)
    uid = request.headers.get(REQUEST_UID)
    return ak_id, ak_sk, sts_token, region, func_name, uid

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
