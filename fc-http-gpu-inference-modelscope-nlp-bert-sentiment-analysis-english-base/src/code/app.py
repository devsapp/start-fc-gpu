from flask import Flask
from flask import request
from flask import Response
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import tablestore
import os
import cv2
import base64
import tempfile
import sys
import traceback
import json
import pymysql


# init flask
app = Flask(__name__)


# init model
semantic_cls = pipeline(Tasks.text_classification,
                        model = './model/damo/nlp_bert_sentiment-analysis_english-base')


# init ots
ots_endpoint = os.environ['OTS_ENDPOINT']
ots_ak_id = os.environ['OTS_AK_ID']
ots_ak_secret = os.environ['OTS_AK_SECRET']
ots_instance = os.environ['OTS_INSTANCE']
ots_table = "mall_comments_mock"
ots_client = tablestore.OTSClient(ots_endpoint, ots_ak_id, ots_ak_secret, ots_instance, logger_name = 'table_store.log')


@app.route('/initialize', methods=['POST'])
def initialize():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Initialize Start RequestId: " + request_id)

    # do your init work, this method only run once.

    print("FC Initialize End RequestId: " + request_id)
    return "OK"


@app.route('/ping', methods=['GET'])
def ping():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Ping Start RequestId: " + request_id)

    # do probe work, this method is used to check app alive or not.
    text = 'Great vacuum cleaner'
    result = semantic_cls(text)
    print(result)

    print("FC Ping End RequestId: " + request_id)
    return "OK"


@app.route('/invoke', methods=['POST'])
def invoke():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # get function input event, data type is bytes, convert as needed
    event = request.get_data()

    # invoke work : input customer comments(RDS) -> NLP model -> output customer comments rating(RDS)
    data = fetch_dataset()
    msg = ""

    try:
        for item in data:
            product_id = item.primary_key[0][1]
            user_id = item.primary_key[1][1]
            comment_content = item.attribute_columns[0][1]
            rating = semantic_cls(comment_content)
            print("product_id=", product_id,
                  "user_id=", user_id,
                  "comment_content[INPUT]=", comment_content,
                  "rating[OUTPUT]=", rating, "\n")
            update_rating(product_id, user_id, comment_content, rating)

        msg = json.dumps(data, ensure_ascii=False, default=str)

    except Exception as e:
        exc_info = sys.exc_info()
        trace = traceback.format_tb(exc_info[2])
        errRet = {
            "message": str(e),
            "stack": trace
        }
        print(errRet)
        print("FC Invoke End RequestId: " + request_id)
        return errRet, 404, [("x-fc-status", "404")]

    print("FC Invoke End RequestId: " + request_id)
    return msg, 200, [("Content-Type", "text/plain")]


def fetch_dataset():
    inclusive_start_primary_key = [('product_id', tablestore.INF_MIN), ('user_id', tablestore.INF_MIN)]
    exclusive_end_primary_key = [('product_id', tablestore.INF_MAX), ('user_id', tablestore.INF_MAX)]
    columns_to_get = []
    limit = 1000
    try:
        consumed, next_start_primary_key, row_list, next_token = ots_client.get_range(
            ots_table, tablestore.Direction.FORWARD,
            inclusive_start_primary_key, exclusive_end_primary_key,
            columns_to_get, limit, max_version = 1)
        all_rows = []
        all_rows.extend(row_list)

        while next_start_primary_key is not None:
            inclusive_start_primary_key = next_start_primary_key
            consumed, next_start_primary_key, row_list, next_token = ots_client.get_range(
                ots_table, tablestore.Direction.FORWARD,
                inclusive_start_primary_key, exclusive_end_primary_key,
                columns_to_get, limit, max_version = 1)
            all_rows.extend(row_list)

        print('Total rows: ', len(all_rows))
        return all_rows
    except tablestore.OTSClientError as e:
        print("get row failed, http_status:%d, error_message:%s" % (e.get_http_status(), e.get_error_message()))
    except tablestore.OTSServiceError as e:
        print("get row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))


def update_rating(product_id, user_id, comment_content, rating):
    labels = rating["labels"]
    scores = rating["scores"]
    positive = 0
    neutral = 0
    negative = 0
    for index in range(len(labels)):
        if labels[index] == "Positive":
            positive = int(scores[index] * 100)
        if labels[index] == "Neutral":
            neutral = int(scores[index] * 100)
        if labels[index] == "Negative":
            negative = int(scores[index] * 100)

    primary_key = [('product_id', product_id),
                   ('user_id', user_id)]
    attribute_columns = [('comment_content', comment_content),
                         ('comment_rating_positive', positive),
                         ('comment_rating_neutral', neutral),
                         ('comment_rating_negative', negative)]
    row = tablestore.Row(primary_key, attribute_columns)
    try :
        consumed, return_row = ots_client.put_row(ots_table, row)
        print ('[%d %d] put row succeed, consume %s write cu.' % (product_id, user_id, consumed.write))
    except tablestore.OTSClientError as e:
        print("[%d %d] put row failed, http_status:%d, error_message:%s" % (product_id, user_id, e.get_http_status(), e.get_error_message()))
    except tablestore.OTSServiceError as e:
        print("[%d %d] put row failed, http_status:%d, error_code:%s, error_message:%s, request_id:%s" % (product_id, user_id, e.get_http_status(), e.get_error_code(), e.get_error_message(), e.get_request_id()))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
