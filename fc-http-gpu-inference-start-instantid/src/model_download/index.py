import os
import urllib.request
import tarfile


def download_and_extract(url, cache_dir, file_name):
    path = cache_dir + "/" + file_name

    print("download:", url)
    print("path:", path)

    f = urllib.request.urlopen(url)
    with open(path, "wb") as local_file:
        local_file.write(f.read())
        local_file.close()

    tar = tarfile.open(path)
    tar.extractall(path=cache_dir)
    tar.close()


def handler(event, context):
    cache_dir = os.getenv('MODEL_CACHE', '/mnt/auto')

    model_url_1 = "https://fc-start-gpu-code-samples-hz.oss-cn-hangzhou.aliyuncs.com/fc-http-gpu-inference-instantid/checkpoints.tar"
    model_url_2 = "https://fc-start-gpu-code-samples-hz.oss-cn-hangzhou.aliyuncs.com/fc-http-gpu-inference-instantid/models.tar"
    model_url_3 = "https://fc-start-gpu-code-samples-hz.oss-cn-hangzhou.aliyuncs.com/fc-http-gpu-inference-instantid/sdid_models.tar"

    download_and_extract(model_url_1, cache_dir, "checkpoints.tar")
    download_and_extract(model_url_2, cache_dir, "models.tar")
    download_and_extract(model_url_3, cache_dir, "sdid_models.tar")

    for root, dirs, files in os.walk(cache_dir):
        print("==root:", root)
        print("dirs:", dirs)
        print("files:", files)

    print("cache_dir:", cache_dir)
    print("download model scuccess!")
    return "succ"
