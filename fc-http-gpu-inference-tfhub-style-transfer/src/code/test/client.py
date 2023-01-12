import sys
import json
import requests

def main(url, content_url, style_url):
    data = {
        "content_url" : content_url,
        "style_url" : style_url
    }
    resp = requests.post(url,
                         data = json.dumps(data),
                         headers = {'Content-Type': 'application/octet-stream'})
    open("output.png", "wb").write(resp.content)
    print("infernece ok, please check output.png")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: client.py <request url> <content image url> <style image url>")
        # eg: python3 ./test/client.py http://127.0.0.1:9000/invoke https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg
    main(sys.argv[1], sys.argv[2], sys.argv[3])
