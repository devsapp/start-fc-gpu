import sys
import json
import requests

def main(url, text):
    resp = requests.post(url,
                         data = text.encode("utf-8"),
                         headers = {'Content-Type': 'text/plain; charset=utf-8'})
    print("infernece ok, result:")
    print(str(resp.content, encoding='utf-8'))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: client.py <request url> <input text>")

    # Usage:
    # python3 ./test/client.py http://127.0.0.1:9000/invoke "您好，阿里云函数计算"
    main(sys.argv[1], sys.argv[2])
