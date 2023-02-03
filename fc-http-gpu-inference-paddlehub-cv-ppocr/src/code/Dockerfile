FROM nvcr.io/nvidia/paddlepaddle:22.12-py3
WORKDIR /usr/src/app
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_VISIBLE_DEVICES=0,1,2,3
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install paddlehub -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install "paddleocr>=2.0.1" -i https://pypi.tuna.tsinghua.edu.cn/simple
ENV HUB_HOME=/usr/src/app/hub_home
COPY . .
CMD [ "python3", "-u", "/usr/src/app/app.py" ]
EXPOSE 9000
