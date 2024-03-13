import os
import sys
import json
import traceback
import tempfile
from flask import Flask, request
from flask import Response
import torch
from PIL import Image
from torchvision import transforms
from modelscope.hub.file_download import model_file_download
import diffusers
from diffusers.utils import load_image
from diffusers.models import ControlNetModel
import cv2
import torch
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis
from pipeline_stable_diffusion_xl_instantid import StableDiffusionXLInstantIDPipeline, draw_kps

instance_model_path = os.getenv('MODEL_CACHE', '/mnt/auto')
checkpoints_path = instance_model_path + "/checkpoints"
models_path = instance_model_path + "/models"
sdid_models_path = instance_model_path + "/sdid_models"
ifaceapp = ""
pipe = ""

# flask app
app = Flask(__name__)

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
    global ifaceapp
    global pipe

    model_control=model_file_download(model_id="InstantX/InstantID", file_path="ControlNetModel/diffusion_pytorch_model.safetensors", cache_dir=checkpoints_path)
    model_control=model_file_download(model_id="InstantX/InstantID", file_path="ControlNetModel/diffusion_pytorch_model.safetensors", cache_dir=checkpoints_path)
    model_ip=model_file_download(model_id="InstantX/InstantID", file_path="ip-adapter.bin", cache_dir=checkpoints_path)

    ifaceapp = FaceAnalysis(name='antelopev2', root=instance_model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    ifaceapp.prepare(ctx_id=0, det_size=(640, 640))

    # prepare models under ./checkpoints
    face_adapter = checkpoints_path + '/InstantX/InstantID/ip-adapter.bin'
    controlnet_path = checkpoints_path + '/InstantX/InstantID/ControlNetModel/'

    # load IdentityNet
    controlnet = ControlNetModel.from_pretrained(controlnet_path, torch_dtype=torch.float16)
    pipe = StableDiffusionXLInstantIDPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", controlnet=controlnet, torch_dtype=torch.float16, cache_dir=sdid_models_path)
    pipe.cuda()

    # load adapter
    pipe.load_ip_adapter_instantid(face_adapter)

    print("FC Initialize End RequestId: " + request_id)
    return "Function is initialized, request_id: " + request_id + "\n"


@app.route('/ping', methods=['GET'])
def ping():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Ping Start RequestId: " + request_id)

    # do health check

    print("FC Ping End RequestId: " + request_id)
    return "Ping OK\n"


@app.route('/invoke', methods=['POST'])
def invoke():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    req = json.loads(request.data)
    image_url = req["image_url"]
    prompt = req["prompt"]
    negative_prompt = req["negative_prompt"]
    print("image_url:", image_url)
    print("prompt:", prompt)
    print("negative_prompt:", negative_prompt)

    fd_out, path_out = tempfile.mkstemp(suffix=".png")
    data = ""

    try:
        # load an image
        face_image = load_image(image_url)

        # prepare face emb
        face_info = ifaceapp.get(cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR))
        face_info = sorted(face_info, key=lambda x:(x['bbox'][2]-x['bbox'][0])*x['bbox'][3]-x['bbox'][1])[-1] # only use the maximum face
        face_emb = face_info['embedding']
        face_kps = draw_kps(face_image, face_info['kps'])

        pipe.set_ip_adapter_scale(0.8)

        # generate image
        image = pipe(prompt, negative_prompt, image_embeds=face_emb, image=face_kps, controlnet_conditioning_scale=0.8).images[0]
        image.save(path_out)

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
        os.remove(path_out)

    print("FC Invoke End RequestId: " + request_id)
    return Response(data, mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
