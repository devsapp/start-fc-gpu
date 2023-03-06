
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、服务名、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco&type=packageDownload">
  </a>
</p>

<description>

快速部署 ModelScope OFA Visual Grounding Large-EN 推理模型至FC-GPU运行环境

</description>

<codeUrl>

- [:smiley_cat: 代码](https://github.com/devsapp/start-fc-gpu)

</codeUrl>
<preview>

- [:eyes: 预览](http://www.devsapp.cn/details.html?name=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco)

</preview>


## 前期准备

使用该项目，您需要有开通以下服务：

<service>

| 服务 |  备注  |
| --- |  --- |
| 函数计算 FC |  用于创建FC服务与函数 |
| 容器镜像服务 CR |  用于从镜像仓库拉取应用镜像 |

</service>

推荐您拥有以下的产品权限 / 策略：
<auth>

| 服务/业务 |  权限 |  备注  |
| --- |  --- |   --- |
| 函数计算 | AliyunFCFullAccess |  用于创建FC服务与函数 |
| 函数计算 | AliyunContainerRegistryFullAccess |  用于从镜像仓库拉取应用镜像 |

</auth>

<remark>

您还需要注意：   
无

</remark>

<disclaimers>

免责声明：   
本项目仅用于相关框架与功能的使用示例，不承担额外的使用风险。

</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco) 该应用。
   
</appcenter>
<deploy>

详见使用文档

</deploy>

## 应用详情

<appdetail id="flushContent">

- OFA(One-For-All)是通用多模态预训练模型，使用简单的序列到序列的学习框架统一模态（跨模态、视觉、语言等模态）和任务（如图片生成、视觉定位、图片描述、图片分类、文本生成等），详见ICML 2022 OFA论文：https://arxiv.org/abs/2202.03052
- 本应用模板基于OFA模型实现了图像语义与视觉定位，预训练数据集为Refcoco。

| input | text | output |
|  ----  | ---- | ----  |
| ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/visual_grounding.png?raw=true) | "a blue turtle-like pokemon with round head"  | ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/visual_grounding_result1.png?raw=true) |
| ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/suitcases.png?raw=true) | "a white suitcases"  | ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/suitcases_result1.png?raw=true) |
| ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/suitcases.png?raw=true) | "a green suitcases"  | ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/suitcases_result2.png?raw=true) |

- 容器环境说明

|  env   |  value  |
|  ----  | ----  |
| Container OS | Ubuntu 20.04 |
| CUDA  | 11.8.0 |
| cuBLAS  | 11.11.3.6 |
| cuDNN   | 8.6.0.163 |
| cuTENSOR  | 1.6.1.5 |
| PyTorch | 1.13.0a0+936e930 |

</appdetail>

## 使用文档

<usedetail id="flushContent">

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco -d fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco`
    - 进入项目，并进行项目部署：`cd fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco && s deploy -y`
    - 检查函数的镜像加速状态:
        - 方式1：`s cli fc api GetFunction -a default --region cn-shenzhen --path '{"serviceName":"fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco-service","functionName":"fc-http-gpu-inference-modelscope-cv-ofa-visual-grounding-refcoco-function"}'` 注意：请将如上default帐号、地域、服务名、函数名替换为
您的项目实际值
        - 方式2：登陆阿里云函数计算控制台，查看该函数的详情页面，确保`镜像加速准备状态`为`可用`
        - ***重要说明：请务必在镜像加速状态完成后进行函数调用，函数计算平台将基于镜像加速技术为您提供大镜像函数调用的冷启动最佳体验；镜像加速状态完成前的函数调用将遭遇冷启动耗时***：
    - 测试项目：
        - 通过脚本调用
            - ```python3 ./test/client.py http://{your_function_http_endpoint}/invoke ./test/imgs/visual_grounding.png "a blue turtle-like pokemon with round head"```
            - ```python3 ./test/client.py http://{your_function_http_endpoint}/invoke ./test/imgs/suitcases.png "a white suitcases"```
            - ```python3 ./test/client.py http://{your_function_http_endpoint}/invoke ./test/imgs/suitcases.png "a green suitcases```

- 根据您选择直接使用官方公开示例镜像、或者从源码构建镜像这2种不同的方式，需要对s.yaml进行一些微调，具体说明如下：
    1. 如果您期望直接使用官方公开示例镜像，请删除或注释actions子配置，这样将在s deploy阶段跳过构建镜像，直接进行部署（官网公开示例镜像均为public镜像，无须构建可直接在函数中使用）。
    2. 如果您期望从源码构建镜像，则保留actions子配置，这样将在s deploy阶段自动构建镜像，然后进行部署。
    - ![图片alt](https://github.com/devsapp/start-fc-gpu/blob/main/materials/s_yaml_config.png?raw=true)

</usedetail>


<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>
