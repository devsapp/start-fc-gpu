# -*- coding: utf-8 -*-
# python2 and python3
from flask import Flask, request
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import tensorflow_hub as hub
import json
import sys
import os
import numpy as np
import PIL
import tensorflow as tf
import traceback
import matplotlib as mpl

app = Flask(__name__)

# load arbitrary-image-stylization-v1-256 model
hub_model = hub.load('./model')

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
    inference_path("./test/img/content.png", "./test/img/style.png")

    print("FC Ping End RequestId: " + request_id)
    return "Ping OK\n"


@app.route('/invoke', methods=['POST'])
def invoke():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # do invoke work : parse json -> get content/style url -> inference
    data = ""
    try:
        req = json.loads(request.data)
        content_url = req["content_url"]
        style_url = req["style_url"]
        inference_url(content_url, style_url)
        with open("output.png", "rb") as file:
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

    print("FC Invoke End RequestId: " + request_id)
    return data, 200, [("Content-Type", "image/png")]


def load_img(path):
    max_dim = 512
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    
    return img


def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


def inference_url(content_url, style_url):
    content_path = tf.keras.utils.get_file("content.png", content_url)
    style_path = tf.keras.utils.get_file("style.png", style_url)
    print("download image ok")

    return inference_path(content_path, style_path)


def inference_path(content_path, style_path):
    mpl.rcParams['figure.figsize'] = (12,12)
    mpl.rcParams['axes.grid'] = False

    content_image = load_img(content_path)
    style_image = load_img(style_path)
    print("load image ok")

    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    tensor_to_image(stylized_image).save("output.png")
    print("generate stylized image ok")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
