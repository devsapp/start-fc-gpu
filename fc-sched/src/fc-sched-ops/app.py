from flask import Flask
from flask import request
from flask import json
from flask import jsonify, make_response
from tablestore import *
import os
import json

OTS_ENDPOINT = os.getenv("OTS_ENDPOINT", "https://fc-sched.cn-beijing.ots.aliyuncs.com")
OTS_INSTANCE = os.getenv("OTS_INSTANCE_NAME", "fc-sched")
OTS_TABLENAME = os.getenv("OTS_TABLE_NAME","endpoints")
REQUEST_ID_HEADER = 'x-fc-request-id'
REQUEST_AK_ID_HEADER = 'x-fc-access-key-id'
REQUEST_AK_SK_HEADER = 'x-fc-access-key-secret'
REQUEST_STS_TOKEN_HEADER = 'x-fc-security-token'

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

    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ip = request.args.get("ip")
    if ip is None:
        return "missing necessary argument: ?ip=x.x.x.x"

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

    print("FC Invoke End RequestId: " + rid)
    return "register succ"

@app.route('/endpoint/unregister', methods=['GET'])
def unregister_endpoint():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    ak_id, ak_sk, sts_token = fetch_ctx_info()
    ip = request.args.get("ip")
    if ip is None:
        return "missing necessary argument: ?ip=x.x.x.x"

    client = OTSClient(OTS_ENDPOINT, ak_id, ak_sk, OTS_INSTANCE, sts_token=sts_token) 
    
    primary_key = [('endpoint', ip)]
    row = Row(primary_key)
    try:
        consumed, return_row = client.delete_row(OTS_TABLENAME, row, None)
    except OTSClientError as e:
        print("unregister endpoint failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print("unregister endpoint failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))

    print("FC Invoke End RequestId: " + rid)
    return "unregister succ"

@app.route('/endpoint/list', methods=['GET'])
def list_endpoint():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)

    ak_id, ak_sk, sts_token = fetch_ctx_info()

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
    except OTSClientError as e:
        print('get row failed, http_status:%d, error_message:%s' % (e.get_http_status(), e.get_error_message()))
    except OTSServiceError as e:
        print('get row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s' % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))

    print("FC Invoke End RequestId: " + rid)
    return make_response(jsonify(output), 200)

def fetch_ctx_info():
    ak_id = request.headers.get(REQUEST_AK_ID_HEADER)
    ak_sk = request.headers.get(REQUEST_AK_SK_HEADER)
    sts_token = request.headers.get(REQUEST_STS_TOKEN_HEADER)
    return ak_id, ak_sk, sts_token

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
