FROM registry.cn-hangzhou.aliyuncs.com/modelscope-repo/modelscope:ubuntu20.04-cuda11.3.0-py37-torch1.11.0-tf1.15.5-1.1.2
WORKDIR /usr/src/app
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update
RUN pip3 install Flask -i https://pypi.tuna.tsinghua.edu.cn/simple
#ENV LD_LIBRARY_PATH=/usr/local/lib/python3.8/dist-packages/nvidia/cublas/lib:$LD_LIBRARY_PATH
#hack: build modelscope's index in docker image building stage to decrease startup cost time
RUN python /opt/conda/lib/python3.7/site-packages/modelscope/utils/ast_utils.py
#COPY hook/ast_utils.py /opt/conda/lib/python3.7/site-packages/modelscope/utils/ast_utils.py
COPY . .
CMD [ "python3", "-u", "/usr/src/app/app.py" ]
EXPOSE 9000
