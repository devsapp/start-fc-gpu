from flask import Flask, request
import paddlehub as hub
import json
import os
import sys
import traceback


# initialize web framework
app = Flask(__name__)
# load LAC model
lac = hub.Module(name="lac")


@app.route('/initialize', methods=['POST'])
def initialize():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Initialize Start RequestId: " + request_id)

    # do your things
    # Use the following code to get temporary credentials
    # access_key_id = request.headers['x-fc-access-key-id']
    # access_key_secret = request.headers['x-fc-access-key-secret']
    # access_security_token = request.headers['x-fc-security-token']

    print("FC Initialize End RequestId: " + request_id)
    return "Function is initialized, request_id: " + request_id + "\n"


@app.route('/ping', methods=['GET'])
def ping():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Ping Start RequestId: " + request_id)

    # do your things
    test_text = ["我是分词测试1", "我是分词测试2"]
    results = lac.cut(text=test_text, use_gpu=True, batch_size=1, return_tag=True)
    for result in results:
        print(result['word'])
        print(result['tag'])

    print("FC Ping End RequestId: " + request_id)
    return "Ping OK\n"


@app.route('/invoke', methods=['POST'])
def invoke():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work : input image -> cv model -> output image
    msg = ""

    try:
        text = request.get_data().decode("utf-8")
        print(text)
        results = lac.cut(text=text, use_gpu=True, batch_size=1, return_tag=True)
        print(results)
        msg = json.dumps(results, ensure_ascii=False)
        print(msg)
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


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
