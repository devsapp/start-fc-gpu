# 阿里云函数计算：FC ServerlessGPU 应用模板案例

![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/logo.png?raw=true)

## 本地快速体验

通过该应用，您可以简单快速的创建一个 FC 案例到阿里云函数计算服务。

- 下载命令行工具：`npm install -g @serverless-devs/s`
- 初始化一个模版项目：`s init start-fc-http-python3`
- 进入项目后部署项目：`cd start-fc && s deploy`

## 包含内容

- ```GPU运行环境检测```
    - [fc-http-gpu-utils-nvidia-smi](fc-http-gpu-utils-nvidia-smi/src)
    - `s init fc-http-gpu-utils-nvidia-smi`
- ```快速部署ModelScope DCT-Net人像卡通化模型至阿里云函数计算GPU实例```
    - [fc-http-gpu-inference-modelscope-cv-dctnet](fc-http-gpu-inference-modelscope-cv-dctnet/src)
    - `s init fc-http-gpu-inference-modelscope-cv-dctnet`
- ```快速部署 PytorchHub Mobilenet v2 推理模型至FC-GPU运行环境``` 
    - [fc-http-gpu-inference-torchhub-cv-mobilenet-v2](fc-http-gpu-inference-torchhub-cv-mobilenet-v2/src) 
    - `s init fc-http-gpu-inference-torchhub-cv-mobilenet-v2`

---

> - Serverless Devs 项目：https://www.github.com/serverless-devs/serverless-devs
> - Serverless Devs 文档：https://docs.serverless-devs.com
> - Serverless Devs 钉钉交流群：33947367
