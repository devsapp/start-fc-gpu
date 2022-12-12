# fc-http-gpu-inference-torchhub-cv-mobilenet-v2 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-inference-torchhub-cv-mobilenet-v2&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-http-gpu-inference-torchhub-cv-mobilenet-v2" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-inference-torchhub-cv-mobilenet-v2&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-http-gpu-inference-torchhub-cv-mobilenet-v2" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-inference-torchhub-cv-mobilenet-v2&type=packageDownload">
  </a>
</p>

<description>

> ***快速部署 PytorchHub Mobilenet v2 推理模型至FC-GPU运行环境***

</description>

<table>

## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 函数计算 |     
| --- |  --- |   
| 权限/策略 | AliyunFCFullAccess</br>AliyunContainerRegistryFullAccess |     


</table>

<codepre id="codepre">



</codepre>

<deploy>

## 部署 & 体验

<appcenter>

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=fc-http-gpu-inference-torchhub-cv-mobilenet-v2) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=fc-http-gpu-inference-torchhub-cv-mobilenet-v2)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init fc-http-gpu-inference-torchhub-cv-mobilenet-v2 -d fc-http-gpu-inference-torchhub-cv-mobilenet-v2`   
    - 进入项目，并进行项目部署：`cd fc-http-gpu-inference-torchhub-cv-mobilenet-v2 && s deploy -y`
    - 检查函数的镜像加速状态:
        - 方式1：`s cli fc api GetFunction -a default --region cn-shenzhen --path '{"serviceName":"fc-http-gpu-inference-torchhub-cv-mobilenet-v2-service","functionName":"fc-http-gpu-inference-torchhub-cv-mobilenet-v2-function"}'` 注意：请将如上default帐号、地域、服务名、函数名替换为
您的项目实际值
        - 方式2：登陆阿里云函数计算控制台，查看该函数的详情页面，确保`镜像加速准备状态`为`可用`
        - ***重要说明：请务必在镜像加速状态完成后进行函数调用，函数计算平台将基于镜像加速技术为您提供大镜像函数调用的冷启动最佳体验；镜像加速状态完成前的函数调用将遭遇冷启动耗时***：
    - 测试项目：
        - 通过脚本调用：`python3 ./code/test/client.py http://{your_function_http_endpoint}/invoke ./code/test/img/dog.jpg`
        - 通过curl调用：`curl -v -X POST -H "Content-Type:application/octet-stream" --data-binary "@./code/test/img/cat.jpg" "http://{your_function_http_endpoint}/invoke"`

- 根据您选择直接使用官方公开示例镜像、或者从源码构建镜像这2种不同的方式，需要对s.yaml进行一些微调，具体说明如下：
    1. 如果您期望直接使用官方公开示例镜像，请删除或注释actions子配置，这样将在s deploy阶段跳过构建镜像，直接进行部署（官网公开示例镜像均为public镜像，无须构建可直接在函数中使用）。
    2. 如果您期望从源码构建镜像，则保留actions子配置，这样将在s deploy阶段自动构建镜像，然后进行部署。
    - ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/s_yaml_config.png?raw=true)

</deploy>

<appdetail id="flushContent">

# 应用详情

- Google在2018年提出MobileNetV2模型，该模型是对MobileNetV1的重大改进，推动了移动视觉识别技术的发展，包括分类、对象检测和语义分割。
- 本应用模板基于MobileNetV2模型实现了图像识别，预训练数据集为ImageNet。
| input | output |
|  ----  | ----  |
| ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/dog.jpg?raw=true) | ```{"Egyptian cat":0.02607746794819832,"Persian cat":0.6318033933639526,"lynx":0.15323816239833832,"tabby":0.048527609556913376,"tiger cat":0.06776202470064163}``` |
| ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/cat.jpg?raw=true) | ```{"Great Pyrenees":0.00988676119595766,"Pomeranian":0.0698879137635231,"Samoyed":0.8303040862083435,"collie":0.01079776231199503,"keeshond":0.012964126653969288}``` |

- 容器环境说明
|  env   |  value  |
|  ----  | ----  |
| Container OS | Ubuntu 20.04 |
| CUDA  | 11.8.0 |
| cuBLAS  | 11.11.3.6 |
| cuDNN	  | 8.6.0.163 |
| cuTENSOR  | 1.6.1.5 |
| PyTorch | 1.13.0a0+936e930 |

</appdetail>

<devgroup>

## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
|--- | --- | --- |
| <center>微信公众号：`serverless`</center> | <center>微信小助手：`xiaojiangwh`</center> | <center>钉钉交流群：`33947367`</center> | 

</p>

</devgroup>
