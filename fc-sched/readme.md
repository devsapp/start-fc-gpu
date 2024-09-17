
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# fc3-sched 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc3-sched&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc3-sched" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc3-sched&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc3-sched" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc3-sched&type=packageDownload">
  </a>
</p>

<description>

FC集群调度应用(fc3.0)

</description>

<codeUrl>

- [:smiley_cat: 代码](https://github.com/devsapp/fc3-sched/tree/v3)

</codeUrl>
<preview>

- [:eyes: 预览](https://github.com/devsapp/fc3-sched/tree/v3)

</preview>

## 前期准备

使用该项目，您需要有开通以下服务并拥有对应权限：

<service>

| 服务/业务 |  权限  | 相关文档 |
| --- |  --- | --- |
| 函数计算 |  创建函数 | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |

</service>

<remark>

</remark>

<disclaimers>
</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=fc3-sched) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=fc3-sched) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init fc3-sched -d fc3-sched`
  - 进入项目，并进行项目部署：`cd fc3-sched && s deploy -y`
   
</deploy>

## 应用介绍

<appdetail id="flushContent">

本应用支持对用户自建IDC GPU集群与云上FC GPU集群进行混合调度，在优先充分利用用户自建IDC GPU集群的基础上，可将超出IDC GPU集群处理能力部分的推理请求调度至云上FC GPU集群。

</appdetail>

## 使用流程

<usedetail id="flushContent">

</usedetail>

## 注意事项

<matters id="flushContent">

* FC函数权限: fc-sched-[core|ops]函数角色可使用默认的aliyunfcdefaultrole, 并为aliyunfcdefaultrole增加AliyunOTSFullAccess权限。
* OTSEndpoint: 需要为OTSEndpint开启公网访问权限、或VPC访问权限; 当OTSEndpint开启VPC访问权限时, 请为fc-sched-[core|ops]配置相同的VPC。


</matters>

<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>
