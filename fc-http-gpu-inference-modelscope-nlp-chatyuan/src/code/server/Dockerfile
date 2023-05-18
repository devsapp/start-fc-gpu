FROM ubuntu:20.04

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak && \
    sed -i "s@http://.*archive.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list && \
    sed -i "s@http://.*security.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list

ENV TZ="Asia/Shanghai"
RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata



RUN apt install ffmpeg libsm6 libxext6 python3 python3-pip  -y
RUN python3 -m pip install "modelscope[nlp]" -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    python3 -m pip install fairseq decord uvicorn fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./pre-download.py /data/pre-download.py
RUN python3 /data/pre-download.py

COPY ./main.py /data/main.py

WORKDIR /data
ENTRYPOINT [ "uvicorn", "main:app" , "--host=0.0.0.0"]

