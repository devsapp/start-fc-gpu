import hashlib
import time
import base64
import hashlib
import os
import sys
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from modelscope.pipelines import pipeline


p = None
initializing = False
cached = {}


def getPipeline():
    global p, initializing

    if p == None:
        if initializing == True:
            while p == None:
                time.sleep(500)
        else:
            initializing = True
            print("start load model")
            p = pipeline(
                'image-captioning',
                'damo/mplug_image-captioning_coco_base_zh'
            )
            print("load model success")
    return p


def getResult(url):
    global cached
    if url not in cached:
        cached[url] = getPipeline()({'image': url})

    return cached[url]


def preCheck(url):
    return cached.get(url, False)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/url")
def read_root(url: str):
    return {"data": getResult(url)}


@app.post("/base64")
def read_root(body=Body()):
    data = base64.b64decode(body)
    md5 = hashlib.md5(data).hexdigest()
    filename = "/tmp/" + md5

    pc = preCheck(md5)
    if pc != False:
        return {"data": pc}

    with open(filename, "wb") as f:
        f.write(data)

    result = getResult(filename)
    os.remove(filename)
    return {"data": result}
