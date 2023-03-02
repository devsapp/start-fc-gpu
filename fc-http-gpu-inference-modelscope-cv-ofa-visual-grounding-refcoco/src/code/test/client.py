import sys
import requests

def main(url, path, text):
    image = open(path, "rb").read()
    params = {"text": text}
    resp = requests.post(url,
                         data = image,
                         headers = {'Content-Type': 'application/octet-stream'},
                         params = params)
    open("output.png", "wb").write(resp.content)
    print("infernece ok, please check output.png")


if __name__ == "__main__":
    # eg1: python3 ./test/client.py http://127.0.0.1:9000/invoke ./test/imgs/visual_grounding.png "a blue turtle-like pokemon with round head"
    # eg2: python3 ./test/client.py http://127.0.0.1:9000/invoke ./test/imgs/suitcases.png "a white suitcases"
    # eg3: python3 ./test/client.py http://127.0.0.1:9000/invoke ./test/imgs/suitcases.png "a green suitcases"

    if len(sys.argv) != 4:
        sys.exit("Usage: client.py <request url> <image path> <query text>")
    main(sys.argv[1], sys.argv[2], sys.argv[3])
