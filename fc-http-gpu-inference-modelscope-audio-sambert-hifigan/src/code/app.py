from flask import Flask
from flask import request
from flask import Response
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from scipy.io.wavfile import write
import traceback
import tempfile
import sys
import os


app = Flask(__name__)
sambert_hifigan_tts = pipeline(task=Tasks.text_to_speech,
                               model='./model/damo/speech_sambert-hifigan_tts_zhiyan_emo_zh-cn_16k')

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

    # do probe work, this method is used to check app alive or not.
    text = "测试模型1，测试模型2，测试模型3"
    output = inference(text)
    wav = output[OutputKeys.OUTPUT_PCM]

    print("FC Ping End RequestId: " + request_id)
    return "Ping OK\n"


@app.route('/invoke', methods=['POST'])
def invoke():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work.
    fd_in, path_in = tempfile.mkstemp()
    data = ""
    
    try:
        text = request.get_data().decode("utf-8")
        output = inference(text)
        pcm = output[OutputKeys.OUTPUT_PCM]
        write(path_in, 16000, pcm)
        with os.fdopen(fd_in, "rb") as file:
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

    print("FC Invoke End RequestId: " + request_id)
    return data, 200, [("Content-Type", "audio/x-wav")]


def inference(text):
    output = sambert_hifigan_tts(input=text)
    return output


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
