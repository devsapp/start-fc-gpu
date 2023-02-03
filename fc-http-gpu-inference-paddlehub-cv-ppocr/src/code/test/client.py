import sys
import requests

def main(url, path):
    image = open(path, "rb").read()
    resp = requests.post(url,
                         data = image,
                         headers = {'Content-Type': 'application/octet-stream'})
    print("response: ", str(resp.content))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: client.py <request url> <image path>")

    # Usage:
    # python3 ./test/client.py http://127.0.0.1:9000/invoke ./test/ppocr_img/imgs_en/img_195.jpg
    main(sys.argv[1], sys.argv[2])
