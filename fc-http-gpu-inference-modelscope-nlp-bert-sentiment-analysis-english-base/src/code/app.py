from flask import Flask
from flask import request
from flask import Response
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os
import cv2
import base64
import tempfile
import sys
import traceback
import json
import pymysql


app = Flask(__name__)
semantic_cls = pipeline(Tasks.text_classification,
                        model = './model/damo/nlp_bert_sentiment-analysis_english-base')


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
            id = item[0]
            user_id = item[1]
            product_id = item[2]
            comment_timestamp = item[3]
            comment_content = item[4]
            rating = semantic_cls(comment_content)
            print("id=", id,
                  "user_id=", user_id,
                  "product_id=", product_id,
                  "comment_timestamp=", comment_timestamp,
                  "comment_content[INPUT]=", comment_content,
                  "rating[OUTPUT]=", rating)
            update_rating(id, rating)

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


def fetch_db_conn():
    try:
        conn = pymysql.connect(
            host = os.environ['MYSQL_HOST'],       # 替换为您的HOST名称。
            port = int(os.environ['MYSQL_PORT']),  # 替换为您的端口号。
            user = os.environ['MYSQL_USER'],       # 替换为您的用户名。
            passwd = os.environ['MYSQL_PASSWORD'], # 替换为您的用户名对应的密码。
            db = os.environ['MYSQL_DBNAME'],       # 替换为您的数据库名称。
            connect_timeout = 5)
        return conn
    except Exception as e:
        logger.error(e)
        logger.error(
            "ERROR: Unexpected error: Could not connect to MySql instance.")
        raise Exception(str(e))


def fetch_dataset():
    conn = fetch_db_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM product_comment_tbl")
            result = cursor.fetchall()
            return result
    finally:
        conn.close()


def update_rating(id, rating):
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

    sql = "UPDATE product_comment_tbl set comment_rating_positive=%d, comment_rating_neutral=%d, comment_rating_negative=%d where id=%d" % (positive, neutral, negative, id)
    print(sql)
    
    conn = fetch_db_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
