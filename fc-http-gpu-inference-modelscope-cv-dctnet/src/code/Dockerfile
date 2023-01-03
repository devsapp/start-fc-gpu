#FROM registry.cn-hangzhou.aliyuncs.com/modelscope-repo/modelscope:ubuntu20.04-cuda11.3.0-py37-torch1.11.0-tf1.15.5-1.0.2
#WORKDIR /usr/src/app
#RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
#RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
#RUN apt-get update
#RUN pip install Flask
#ENV LD_LIBRARY_PATH=/usr/local/lib/python3.8/dist-packages/nvidia/cublas/lib:$LD_LIBRARY_PATH
#COPY . .
# hack: build modelscope's index in docker image building stage to decrease startup cost time
#RUN python /opt/conda/lib/python3.7/site-packages/modelscope/utils/ast_utils.py
#RUN patch -d /opt/conda/lib/python3.7/site-packages/modelscope/utils -p0 < /usr/src/app/hook/ast_utils.patch
#CMD [ "python3", "-u", "/usr/src/app/app.py" ]
#EXPOSE 9000

#FROM tensorflow/tensorflow:2.7.4-gpu


FROM nvidia/cuda:11.3.0-cudnn8-runtime-ubuntu20.04
WORKDIR /usr/src/app
ENV TZ=Asia/Shanghai
ENV CONDA_DIR=/opt/conda
ENV PATH=/opt/conda/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV ARCH=x86_64
ENV DEBIAN_FRONTEND=non-interactive
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update && apt-get install -y --reinstall ca-certificates && apt-get install -y locales wget git vim ffmpeg libsm6 tzdata language-pack-zh-hans ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy libxext6 build-essential ninja-build && wget https://packagecloud.io/github/git-lfs/packages/debian/bullseye/git-lfs_3.2.0_amd64.deb/download -O ./git-lfs_3.2.0_amd64.deb && dpkg -i ./git-lfs_3.2.0_amd64.deb && rm -f ./git-lfs_3.2.0_amd64.deb
#RUN locale-gen zh_CN && locale-gen zh_CN.utf8 && update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 LANGUAGE=zh_CN.UTF-8 && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install -y python3.7 python3-pip
RUN pip install --no-cache-dir torch==1.12.0 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install --no-cache-dir tensorflow==1.15.5 -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install --upgrade tensorflow-gpu==1.15 -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install "modelscope[cv]" -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip3 install "modelscope==1.0.2" -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install Flask
ENV LD_LIBRARY_PATH=/usr/local/lib/python3.8/dist-packages/nvidia/cublas/lib:$LD_LIBRARY_PATH
# hack: build modelscope's index in docker image building stage to decrease startup cost time
#RUN python /usr/local/lib/python3.8/dist-packages/modelscope/utils/ast_utils.py
#COPY hook/ast_utils.py /usr/local/lib/python3.8/dist-packages/modelscope/utils/ast_utils.py
#COPY . .
#CMD [ "python3", "-u", "/usr/src/app/app.py" ]
#EXPOSE 9000