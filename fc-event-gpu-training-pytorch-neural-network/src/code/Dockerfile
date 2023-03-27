FROM pytorch/pytorch
WORKDIR /usr/src/app
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y python3
COPY . .
CMD [ "python3", "-u", "/usr/src/app/app.py" ]
