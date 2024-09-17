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

OTS_ENDPOINT = os.getenv("OTS_ENDPOINT", "https://fc-sched.cn-beijing.ots.aliyuncs.com")
OTS_INSTANCE = os.getenv("OTS_INSTANCE_NAME", "fc-sched")
OTS_TABLENAME = os.getenv("OTS_TABLE_NAME","endpoints")
REQUEST_ID_HEADER = 'x-fc-request-id'
REQUEST_AK_ID_HEADER = 'x-fc-access-key-id'
REQUEST_AK_SK_HEADER = 'x-fc-access-key-secret'
REQUEST_STS_TOKEN_HEADER = 'x-fc-security-token'
REQUEST_REGION_HEADER = 'x-fc-region'
REQUEST_FUNCTION_NAME_HEADER = 'x-fc-function-name'
REQUEST_UID = 'x-fc-account-id'

app = Flask(__name__)

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

    # step1: register in database
    ip = request.args.get("ip")
    if ip is None:
        return "missing necessary argument: ?ip=x.x.x.x"

    ak_id, ak_sk, sts_token, _, _, _ = fetch_ctx_info()
    client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    primary_key = [('endpoint', ip)]
    attribute_columns = [('ref', 0)]
    row = Row(primary_key, attribute_columns)
    try:
        consumed, return_row = client.put_row(OTS_TABLENAME, row)
    except OTSClientError as e:
        print("register endpoint failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print("register endpoint failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))                    
    except Exception as e:
        print("register endpoint failed, error_message:%s" % e.get_error_message())

    # step2: setup concurrency & provision for fc-sched-core
    do_sync_concurrency_and_provision(True)

    print("FC Invoke End RequestId: " + rid)
    return "register succ"

@app.route('/endpoint/unregister', methods=['GET'])
def unregister_endpoint():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    # step1: unregister in database
    ip = request.args.get("ip")
    if ip is None:
        return "missing necessary argument: ?ip=x.x.x.x"

    ak_id, ak_sk, sts_token, _, _, _ = fetch_ctx_info()
    client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    primary_key = [('endpoint', ip)]
    row = Row(primary_key)
    try:
        consumed, return_row = client.delete_row(OTS_TABLENAME, row, None)
    except OTSClientError as e:
        print("unregister endpoint failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print("unregister endpoint failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))
    except Exception as e:
        print("unregister endpoint failed, error_message:%s" % e.get_error_message())

    # step2: setup concurrency & provision for fc-sched-core
    do_sync_concurrency_and_provision(False)

    print("FC Invoke End RequestId: " + rid)
    return "unregister succ"

@app.route('/endpoint/list', methods=['GET'])
def list_endpoint():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    output = fetch_endpoints()

    print("FC Invoke End RequestId: " + rid)
    return make_response(jsonify(output), 200)

def fetch_endpoints():
    ak_id, ak_sk, sts_token, _, _, _ = fetch_ctx_info()
    client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    inclusive_start_primary_key = [('endpoint', INF_MIN)]
    exclusive_end_primary_key = [('endpoint', INF_MAX)]
    limit = 5000
    output = []
    try:
        consumed, next_start_primary_key, row_list, next_token = client.get_range(
            OTS_TABLENAME, Direction.FORWARD,
            inclusive_start_primary_key, exclusive_end_primary_key,
            limit = limit)

        all_rows = []
        all_rows.extend(row_list)

        while next_start_primary_key is not None:
            inclusive_start_primary_key = next_start_primary_key
            consumed, next_start_primary_key, row_list, next_token = client.get_range(
                OTS_TABLENAME, Direction.FORWARD,
                inclusive_start_primary_key, exclusive_end_primary_key,
                limit = limit)
            all_rows.extend(row_list)

        for row in all_rows:
            print(row.primary_key, row.attribute_columns)
            output.append( { "endpoint" : row.primary_key[0][1], "ref" : row.attribute_columns[0][1] } )
            #eg: [('endpoint', '11.22.33.55')] [('ref', 0, 1713529197733)]
            #output[row.primary_key[0][1]] = row.attribute_columns[0][1]
        print('Total rows: ', len(all_rows))
        print("output: ", output)
        return output
    except OTSClientError as e:
        print('get row failed, http_status:%d, error_message:%s' % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print('get row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s' % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))
    return []

def do_sync_concurrency_and_provision(inc):
    ak_id, ak_sk, sts_token, region, func_ops_name, uid = fetch_ctx_info()
    client = create_fc_client(region, ak_id, ak_sk, sts_token, uid)
    func_core_name = fetch_core_func_name(func_ops_name)
    n = len(fetch_endpoints())

    if inc == True:
        # sync concurrency before provision
        do_put_concurrency(client, func_core_name, n)
        do_put_provision(client, func_core_name, n)
    else:
        # sync provision before concurrency
        do_put_provision(client, func_core_name, n)
        do_put_concurrency(client, func_core_name, n)

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
    except Exception as error:
        print(error.message)
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)

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
    except Exception as error:
        print(error.message)
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)

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
