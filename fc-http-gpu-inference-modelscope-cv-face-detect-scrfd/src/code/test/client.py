import sys
import requests

def main(url, path):
    image = open(path, "rb").read()
    resp = requests.post(url,
                         data = image,
                         headers = {'Content-Type': 'application/octet-stream'})
    open("output.png", "wb").write(resp.content)
    print("infernece ok, please check output.png")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: client.py <request url> <image path>")
    main(sys.argv[1], sys.argv[2])
