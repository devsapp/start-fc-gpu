import os
import requests
import tarfile


def download_and_extract(url, cache_dir, file_name):
    path = cache_dir + "/" + file_name

    print("download:", url)
    print("path:", path)

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)

    tar = tarfile.open(path)
    tar.extractall(path=cache_dir)
    tar.close()

def download_and_extract_necessary(url, cache_dir, file_name):
    path = cache_dir + "/" + file_name + "_exist"

    # check download?
    if os.path.exists(path):
        print("url exist: ", url)
        return

    download_and_extract(url, cache_dir, file_name)

    # set download flag
    with open(path, 'w') as f:
        print("url download succ: ", url)
        f.write('exist')


def handler(event, context):
    cache_dir = os.getenv('MODEL_CACHE', '/mnt/auto')
    print("cache_dir:", cache_dir)

    # TODO: support more region
    model_url_1 = "https://fc-start-gpu-code-samples-jp.oss-ap-northeast-1-internal.aliyuncs.com/fc-http-gpu-inference-instantid/checkpoints.tar"
    model_url_2 = "https://fc-start-gpu-code-samples-jp.oss-ap-northeast-1-internal.aliyuncs.com/fc-http-gpu-inference-instantid/models.tar"
    model_url_3 = "https://fc-start-gpu-code-samples-jp.oss-ap-northeast-1-internal.aliyuncs.com/fc-http-gpu-inference-instantid/sdid_models.tar"

    download_and_extract_necessary(model_url_1, cache_dir, "checkpoints.tar")
    download_and_extract_necessary(model_url_2, cache_dir, "models.tar")
    download_and_extract_necessary(model_url_3, cache_dir, "sdid_models.tar")


    print("download model scuccess!")
    return "succ"
