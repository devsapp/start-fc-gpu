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


app = Flask(__name__)
ofa_pipe = pipeline(Tasks.visual_grounding, model='./model/damo/ofa_visual-grounding_refcoco_large_en', preprocessor=None)


@app.route('/initialize', methods=['POST'])
def initialize():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Initialize Start RequestId: " + request_id)

    # do your init work, this method only run once.
    # eg: prewarm model

    print("FC Initialize End RequestId: " + request_id)
    return "OK"


@app.route('/ping', methods=['GET'])
def ping():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Ping Start RequestId: " + request_id)

    # do probe work, this method is used to check app alive or not.
    image = './test/imgs/visual_grounding.png'
    text = 'a blue turtle-like pokemon with round head'
    input = {'image': image, 'text': text}
    result = ofa_pipe(input)
    print(result[OutputKeys.BOXES])

    print("FC Ping End RequestId: " + request_id)
    return "OK"


@app.route('/invoke', methods=['POST'])
def invoke():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work : input image, query text -> cv model -> output image
    fd_in, path_in = tempfile.mkstemp()
    fd_out, path_out = tempfile.mkstemp(suffix=".png")
    data = ""

    try:
        # fetch request image
        with os.fdopen(fd_in, 'wb') as file:
            file.write(request.data)
            file.flush()
            file.close()

        # fetch request query
        args = request.args.to_dict()
        text = args.get("text")

        # inference
        input = {'image': path_in, 'text': text}
        result = ofa_pipe(input)
        print(input)
        print(result[OutputKeys.BOXES])

        # generate output image
        img = cv2.imread(path_in, cv2.IMREAD_COLOR)
        cv2.rectangle(img, (int(result[OutputKeys.BOXES][0][0]), int(result[OutputKeys.BOXES][0][1])), (int(result[OutputKeys.BOXES][0][2]), int(result[OutputKeys.BOXES][0][3])), (0,0,255), 2)
        cv2.imwrite(path_out, img)

        with os.fdopen(fd_out, "rb") as file:
            data = file.read()
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
    finally:
        os.remove(path_in)
        os.remove(path_out)

    print("FC Invoke End RequestId: " + request_id)
    return Response(data, mimetype="image/png")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
