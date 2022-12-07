# fc-http-gpu-utils-nvidia-smi 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-utils-nvidia-smi&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-http-gpu-utils-nvidia-smi" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-utils-nvidia-smi&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-http-gpu-utils-nvidia-smi" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-http-gpu-utils-nvidia-smi&type=packageDownload">
  </a>
</p>

<description>

> ***快速检测阿里云函数计算GPU实例的GPU运行环境***

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

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=fc-http-gpu-utils-nvidia-smi) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=fc-http-gpu-utils-nvidia-smi)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init fc-http-gpu-utils-nvidia-smi -d fc-http-gpu-utils-nvidia-smi`   
    - 进入项目，并进行项目部署：`cd fc-http-gpu-utils-nvidia-smi && s deploy -y`
    - 检查函数的镜像加速状态
        - 方式1：`s cli fc api GetFunction -a default --region cn-shenzhen --path '{"serviceName":"fc-http-gpu-utils-nvidia-smi-service","functionName":"fc-http-gpu-utils-nvidia-smi-function"}'` 注意：请将如上default帐号、地域、服务名、函数名替换为您的项目实际值
        - 方式2：登陆阿里云函数计算控制台，查看该函数的详情页面，确保`镜像加速准备状态`为`可用`	
        - ***重要说明：请务必在镜像加速状态完成后进行函数调用，函数计算平台将基于镜像加速技术为您提供大镜像函数调用的冷启动最佳体验；镜像加速状态完成前的函数调用将遭遇冷启动耗时***：
    - 测试项目：
        - 查看GPU实例中所有GPU UUID : `curl -v -X POST "http://fc-httpfunction-fc-http-service-hajpbarcmd.cn-shenzhen.fcapp.run/invoke?mode=list"`
        - 查看GPU实例中所有GPU 详细信息 : `curl -v -X POST "http://fc-httpfunction-fc-http-service-hajpbarcmd.cn-shenzhen.fcapp.run/invoke?mode=details"`


</deploy>

<appdetail id="flushContent">

# 应用详情

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
