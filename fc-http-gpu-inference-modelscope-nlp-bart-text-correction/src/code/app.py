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


app = Flask(__name__)
correct_pipeline = pipeline(task=Tasks.text_error_correction,
                               model='./model/damo/nlp_bart_text-error-correction_chinese')


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
    text = '我们过了江，进了车站。我买票，他忙着照看行李。行李太多了，得向脚夫行些小费，才可过去。他便又忙着和他们讲价钱。我那时真是聪明过分，总觉他说话不大漂亮，非自己插嘴不可。但他终于讲定了价钱；就送我上车。他给我拣定了靠车门的一张椅子；我将他给我做的紫毛大衣铺好坐位。他嘱我路上小心，夜里警醒些，不要受凉。又嘱托茶房好好照应我。我心里暗笑他的迂；他们只认得钱，托他们直是白托！而且我这样大年纪的人，难道还不能料理自己么？唉，我现在想想，那时真是太聪明了！'
    result = correct_pipeline(text)
    print(result)

    print("FC Ping End RequestId: " + request_id)
    return "OK"


@app.route('/invoke', methods=['POST'])
def invoke():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work : input image -> cv model -> output image
    data = ""

    try:
        text = request.get_data().decode("utf-8")
        print(text)

        result = correct_pipeline(text)

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
