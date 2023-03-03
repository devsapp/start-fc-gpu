FROM registry.cn-hangzhou.aliyuncs.com/modelscope-repo/modelscope:ubuntu20.04-cuda11.3.0-py37-torch1.11.0-tf1.15.5-1.3.0 AS build_base
COPY build.py .
RUN python build.py

FROM registry.cn-hangzhou.aliyuncs.com/modelscope-repo/modelscope:ubuntu20.04-cuda11.3.0-py37-torch1.11.0-tf1.15.5-1.3.0
WORKDIR /usr/src/app
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN pip install Flask
COPY --from=build_base /mnt/workspace/.cache/modelscope /mnt/workspace/.cache/modelscope
COPY --from=build_base /tmp/model /usr/src/app/model
COPY . .
CMD [ "python3", "-u", "/usr/src/app/app.py" ]
EXPOSE 9000
