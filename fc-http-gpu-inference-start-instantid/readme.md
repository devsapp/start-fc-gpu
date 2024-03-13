# start-instantid 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-instantid&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-instantid" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-instantid&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=start-instantid" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=start-instantid&type=packageDownload">
  </a>
</p>

<description>

> ***快速运行InstantID模型在阿里云函数计算GPU实例***

[InstantID 魔搭社区](https://modelscope.cn/models/instantx/InstantID/summary)
[InstantID 开源项目](https://github.com/InstantID/InstantID)

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

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=start-instantid) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=start-instantid)  该应用。

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init start-instantid -d start-instantid`
    - 部署项目：`cd start-instantid && s deploy -y`
- 测试方法
    - [测试脚本](https://github.com/devsapp/start-fc-gpu/blob/main/fc-http-gpu-inference-start-instantid/src/model_app/test/client.py)
    - `python3 ./test/client.py http://127.0.0.1:9000/invoke "http://dapengtmp.oss-cn-shanghai.aliyuncs.com/gpu/demo_face.png" "analog film photo of a man. faded film, desaturated, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage, masterpiece, best quality" "lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured (lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch,deformed, mutated, cross-eyed, ugly, disfigured"`
检查函数的镜像加速状态:


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
