from flask import Flask, render_template, request
import os
import sys
import traceback
import pymysql

app = Flask(__name__, template_folder="./template")


@app.route('/initialize', methods=['POST'])
def initialize():
    # See FC docs for all the HTTP headers: https://www.alibabacloud.com/help/doc-detail/132044.htm#common-headers
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Initialize Start RequestId: " + request_id)

    # do your things
    # Use the following code to get temporary credentials
    # access_key_id = request.headers['x-fc-access-key-id']
    # access_key_secret = request.headers['x-fc-access-key-secret']
    # access_security_token = request.headers['x-fc-security-token']

    print("FC Initialize End RequestId: " + request_id)
    return "Function is initialized, request_id: " + request_id + "\n"


@app.route('/invoke', methods=['GET'])
def invoke():
    # See FC docs for all the HTTP headers: https://www.alibabacloud.com/help/doc-detail/132044.htm#common-headers
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    try:
        data = fetch_dataset()
        return render_template("rating.html", data = data)
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
        exc_info = sys.exc_info()
        trace = traceback.format_tb(exc_info[2])
        errRet = {
            "message": str(e),
            "stack": trace
        }
        print(errRet)
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


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)

