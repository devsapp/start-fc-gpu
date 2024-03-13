# syntax = docker/dockerfile:experimental
# README:
#     1. the current source code forked from https://github.com/InstantID/InstantID
#     2. 
FROM registry.us-west-1.aliyuncs.com/modelscope-repo/modelscope:ubuntu22.04-cuda12.1.0-py310-torch2.1.2-tf2.14.0-1.12.0
WORKDIR /usr/src/app
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
RUN pip install flask
RUN pip install insightface==0.7.3
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:32
COPY ./InstantID ./
COPY ./app.py ./
CMD [ "python3", "-u", "/usr/src/app/app.py" ]
EXPOSE 9000
