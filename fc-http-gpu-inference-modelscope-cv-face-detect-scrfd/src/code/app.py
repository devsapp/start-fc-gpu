from modelscope.utils.cv.image_utils import draw_face_detection_result
from modelscope.preprocessors.image import LoadImage
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from flask import Flask
from flask import request
from flask import Response
import matplotlib.pyplot as plt
import os
import cv2
import sys
import traceback
import tempfile


app = Flask(__name__)
face_detection = pipeline(Tasks.face_detection, model='./model/damo/cv_resnet_facedetection_scrfd10gkps')


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
    img_path = './test/img/face_detection2.jpeg'
    result = face_detection(img_path)
    print(result)

    print("FC Ping End RequestId: " + request_id)
    return "OK"


@app.route('/invoke', methods=['POST'])
def invoke():
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work : input image -> cv model -> output image
    fd_in, path_in = tempfile.mkstemp()
    fd_out, path_out = tempfile.mkstemp(suffix=".png")
    data = ""

    try:
        with os.fdopen(fd_in, 'wb') as file:
            file.write(request.data)
            file.flush()
            file.close()

        # inference
        result = face_detection(path_in)
        img = LoadImage.convert_to_ndarray(path_in)
        cv2.imwrite(path_out, img)
        img_draw = draw_face_detection_result(path_out, result)
        plt.imsave(path_out, img_draw)

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
