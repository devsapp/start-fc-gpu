# -*- coding: utf-8 -*-
# python2 and python3
from __future__ import print_function
from http.server import HTTPServer, BaseHTTPRequestHandler
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import json
import sys
import logging
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import PIL
import tensorflow as tf
import pathlib
import urllib.request
import random

class Resquest(BaseHTTPRequestHandler):
    def upload(self, url, path):
        print("enter upload:", url)
        headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': os.stat(path).st_size,
        }
        req = urllib.request.Request(url, open(path, 'rb'), headers=headers, method='PUT')
        urllib.request.urlopen(req)

    def tensor_to_image(self, tensor):
        tensor = tensor*255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor)>3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
        return PIL.Image.fromarray(tensor)
    
    def load_img(self, path_to_img):
        max_dim = 512
        img = tf.io.read_file(path_to_img)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)

        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]
        return img

    def do_style_transfer(self):
        mpl.rcParams['figure.figsize'] = (12,12)
        mpl.rcParams['axes.grid'] = False

        #content_path = tf.keras.utils.get_file('YellowLabradorLooking_new.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg')
        #style_path = tf.keras.utils.get_file('kandinsky5.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg')
        content_path = tf.keras.utils.get_file(str(random.randint(0,100000000)) + ".jpg", 'https://dapeng-fc-test.oss-cn-shanghai.aliyuncs.com/c1.png')
        style_path = tf.keras.utils.get_file(str(random.randint(0,100000000)) + ".jpg",'https://dapeng-fc-test.oss-cn-shanghai.aliyuncs.com/c2.png')

        content_image = self.load_img(content_path)
        style_image = self.load_img(style_path)
        print("load image ok")

        stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
        print("load model ok")

        path = "/tmp/" + str(random.randint(0,100000000)) + ".png"
        self.tensor_to_image(stylized_image).save(path)
        print("generate stylized image ok")

        self.upload("https://dapeng-fc-test.oss-cn-shanghai.aliyuncs.com/stylized-image.png" ,path)        
        return "transfer ok"
        
    def style_transfer(self):
        msg = self.do_style_transfer()
        data = {"result": msg}
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def pong(self):
        data = {"function":"tf_style_transfer"}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        
    def dispatch(self):
        # check path
        if self.path == '/ping':
            self.style_transfer()
            return

        # check header
        mode = self.headers.get('RUN-MODE')
        if mode == "ping":
            self.pong()
        elif mode == "normal":
            self.style_transfer()
        else:
            self.pong()
    
    def do_GET(self):
        self.dispatch()
        
    def do_POST(self):
        self.dispatch()        

if __name__ == "__main__":
    host = ("0.0.0.0", 9000)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()


##########################################################################

import os
import sys
import traceback
import tempfile
from flask import Flask, request
import tensorflow_hub as hub

app = Flask(__name__)

# load arbitrary-image-stylization-v1-256 model
hub_model = hub.load('/usr/src/app/style_transfer_model')


        # Load MobileNet v2 model
torch.hub.set_dir("./model/torch/hub")
model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=True)
model.eval()

# Load the categories
with open("imagenet_classes.txt", "r") as f:
    categories = [s.strip() for s in f.readlines()]


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


@app.route('/ping', methods=['POST'])
def ping():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Ping Start RequestId: " + request_id)

    # do your things
    top5_prob, top5_catid = inference("./test/img/dog.jpg")
    for i in range(top5_prob.size(0)):
        print(categories[top5_catid[i]], top5_prob[i].item())

    print("FC Ping End RequestId: " + request_id)
    return "Ping OK\n"


@app.route('/invoke', methods=['POST'])
def invoke():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work : input image -> cv model -> output image
    fd_in, path_in = tempfile.mkstemp()
    msg = {}

    try:
        with os.fdopen(fd_in, 'wb') as file:
            file.write(request.data)
            file.flush()

        # inference
        top5_prob, top5_catid = inference(path_in)
        for i in range(top5_prob.size(0)):
            msg[categories[top5_catid[i]]] = top5_prob[i].item()
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


def inference(content_path, style_path):
    return ""


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
