import requests
import base64

endpoint="http://39.100.103.2:7860"    # backend ecs1
endpoint="http://47.92.208.112:7860"   # backend ecs2
endpoint="http://fc-sched-core-efqkxjhmge.cn-zhangjiakou.fcapp.run"  # frontend fc endpoint(ecs1+ec2)
endpoint="http://sd-641206--sd.fcv3.1431999136518149.cn-hangzhou.fc.devsapp.net" # fc endpoint(fc native gpu)
endpoint="http://fc-sched-proxy-hapgaagkif.cn-zhangjiakou.fcapp.run" # fc hybrid endpoint(user face)
username=""
password=""

resp = requests.post(
    "%s/sdapi/v1/txt2img" % endpoint,
    #headers={
    #    "Authorization": "Basic %s" % (base64.b64encode(("%s:%s" % (username, password)).encode("utf-8")).decode("utf-8")), # 如果未开启 API 鉴权，可忽略该部分
    #},
    json={
        "prompt": "1 girl, sunshine, dog",
        "step": 10,
        "height": 512,
        "width": 1024,
        
        "override_settings": { 
            # "sd_model_checkpoint": "mixProV4.Cqhm.safetensors",
            "sd_model_checkpoint": "majicMIX realistic_v6.safetensors",
        },
    }
)

if resp.status_code == 200:
    data = resp.json()
    for i, img in enumerate(data["images"]):
        with open("%s.png" % (i), "wb") as f:
            b = base64.b64decode(img)
            f.write(b)
    data["images"] = ""
    print(data)
else:
    print(resp.status_code, resp.text)
