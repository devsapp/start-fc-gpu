from flask import Flask, request
import paddlehub as hub
import json
import os
import sys
import traceback


# initialize web framework
app = Flask(__name__)
# load pron-detection LSTM model
porn_detection_lstm = hub.Module(name="porn_detection_lstm")


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
    test_text = ["黄片下载", "打击黄牛党"]
    results = porn_detection_lstm.detection(texts=test_text, use_gpu=True, batch_size=1)

    for index, text in enumerate(test_text):
        results[index]["text"] = text
    for index, result in enumerate(results):
        print(results[index])

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

        results = porn_detection_lstm.detection(texts=[text], use_gpu=True, batch_size=1)
        for index, result in enumerate(results):
            print(results[index])

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
