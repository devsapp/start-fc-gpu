FROM nvidia/cuda:11.3.1-devel-ubuntu18.04
WORKDIR /usr/src/app
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD [ "python3", "-u", "/usr/src/app/app.py" ]
EXPOSE 9000