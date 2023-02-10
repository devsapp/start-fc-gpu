from flask import Flask, request
from paddleocr import PaddleOCR
import json
import os
import sys
import traceback
import tempfile


# initialize web framework
app = Flask(__name__)
# load ppocr model : need to run only once to download and load model into memory
ocr = PaddleOCR(use_angle_cls=True, lang='en')


@app.route('/initialize', methods=['POST'])
def initialize():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Initialize Start RequestId: " + request_id)

    # do your things: pre-warm-up paddleocr 
    ping()

    print("FC Initialize End RequestId: " + request_id)
    return "Function is initialized, request_id: " + request_id + "\n"


@app.route('/ping', methods=['GET'])
def ping():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Ping Start RequestId: " + request_id)

    # do your things
    img_path = './test/ppocr_img/imgs_en/img_12.jpg'
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)

    print("FC Ping End RequestId: " + request_id)
    return "Ping OK\n"


@app.route('/benchmark', methods=['GET'])
def benchmark():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Ping Start RequestId: " + request_id)

    # do your things
    img_path = [
        './test/ppocr_img/imgs_en/254.jpg',
        './test/ppocr_img/imgs_en/img623.jpg',
        './test/ppocr_img/imgs_en/img_10.jpg',
        './test/ppocr_img/imgs_en/img_11.jpg',
        './test/ppocr_img/imgs_en/img_12.jpg',
        './test/ppocr_img/imgs_en/img_195.jpg',
        './test/ppocr_img/imgs_en/model_prod_flow_en.png',
        './test/ppocr_img/imgs/00006737.jpg',
        './test/ppocr_img/imgs/00009282.jpg',
        './test/ppocr_img/imgs/00015504.jpg',
        './test/ppocr_img/imgs/00018069.jpg',
        './test/ppocr_img/imgs/00056221.jpg',
        './test/ppocr_img/imgs/00057937.jpg',
        './test/ppocr_img/imgs/00059985.jpg',
        './test/ppocr_img/imgs/00077949.jpg',
        './test/ppocr_img/imgs/00111002.jpg',
        './test/ppocr_img/imgs/00207393.jpg',
        './test/ppocr_img/imgs/1.jpg',
        './test/ppocr_img/imgs/11.jpg',
        './test/ppocr_img/imgs/12.jpg',
        './test/ppocr_img/imgs/french_0.jpg',
        './test/ppocr_img/imgs/ger_1.jpg',
        './test/ppocr_img/imgs/ger_2.jpg',
        './test/ppocr_img/imgs/japan_1.jpg',
        './test/ppocr_img/imgs/japan_2.jpg',
        './test/ppocr_img/imgs/korean_1.jpg',
        './test/ppocr_img/imgs/model_prod_flow_ch.png',
        './test/ppocr_img/imgs_words/ch/word_1.jpg',
        './test/ppocr_img/imgs_words/ch/word_2.jpg',
        './test/ppocr_img/imgs_words/ch/word_3.jpg',
        './test/ppocr_img/imgs_words/ch/word_4.jpg',
        './test/ppocr_img/imgs_words/ch/word_5.jpg',
        './test/ppocr_img/imgs_words/en/word_1.png',
        './test/ppocr_img/imgs_words/en/word_2.png',
        './test/ppocr_img/imgs_words/en/word_3.png',
        './test/ppocr_img/imgs_words/en/word_4.png',
        './test/ppocr_img/imgs_words/en/word_5.png',
        './test/ppocr_img/table/1.png',
        './test/ppocr_img/table/layout.jpg',
        './test/ppocr_img/table/paper-image.jpg',
        './test/ppocr_img/table/pipeline_en.jpg',
        './test/ppocr_img/table/pipeline.jpg',
        './test/ppocr_img/table/ppstructure.GIF',
        './test/ppocr_img/table/result_all.jpg',
        './test/ppocr_img/table/result_text.jpg',
        './test/ppocr_img/table/table.jpg',
        './test/ppocr_img/table/tableocr_pipeline_en.jpg',
        './test/ppocr_img/table/tableocr_pipeline.jpg'
    ]
    for idx in range(len(img_path)):
        result = ocr.ocr(img_path[idx], cls=True)

    print("FC Ping End RequestId: " + request_id)
    return "Ping OK\n"


@app.route('/invoke', methods=['POST'])
def invoke():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work : input image -> ocr model -> output result
    fd_in, path_in = tempfile.mkstemp()
    msg = {}

    try:
        with os.fdopen(fd_in, 'wb') as file:
            file.write(request.data)
            file.flush()

        # inference
        result = ocr.ocr(path_in, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)

        msg = json.dumps(result)
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

    print(msg)
    print("FC Invoke End RequestId: " + request_id)
    return msg, 200, [("Content-Type", "text/plain")]


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
