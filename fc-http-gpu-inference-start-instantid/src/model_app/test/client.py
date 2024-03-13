import sys
import json
import requests

def main(url, image_url, prompt, negative_prompt):
    data = {
        "image_url" : image_url,
        "prompt" : prompt,
        "negative_prompt" : negative_prompt,
    }
    resp = requests.post(url,
                         data = json.dumps(data),
                         headers = {'Content-Type': 'application/octet-stream'})
    open("output.png", "wb").write(resp.content)
    print("infernece ok, please check output.png")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit("Usage: client.py <request url> <image url> <\"prompt\"> <\"negative prompt\">")

    # Usage:
    # python3 ./test/client.py http://127.0.0.1:9000/invoke "http://dapengtmp.oss-cn-shanghai.aliyuncs.com/gpu/demo_face.png" "analog film photo of a man. faded film, desaturated, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage, masterpiece, best quality" "lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured (lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch,deformed, mutated, cross-eyed, ugly, disfigured"
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
