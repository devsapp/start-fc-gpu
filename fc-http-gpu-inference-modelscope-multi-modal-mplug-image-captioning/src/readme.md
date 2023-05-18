
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、服务名、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# fc-mplug-image-captioning 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-mplug-image-captioning&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-mplug-image-captioning" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-mplug-image-captioning&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=fc-mplug-image-captioning" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=fc-mplug-image-captioning&type=packageDownload">
  </a>
</p>

<description>

使用serverless devs将fc-mplug-image-captioning部署到阿里云函数计算上

</description>

<codeUrl>

- [:smiley_cat: 代码](https://github.com/devsapp/start-fc-gpu/tree/main/fc-mplug-image-captioning)

</codeUrl>
<preview>



</preview>


## 前期准备

使用该项目，您需要有开通以下服务：

<service>



| 服务 |  备注  |
| --- |  --- |
| 函数计算 FC |  该应用部署于阿里云函数计算 |

</service>

推荐您拥有以下的产品权限 / 策略：
<auth>
</auth>

<remark>

您还需要注意：   
1. 默认使用 CPU 进行模型推理，这可以节省您的资费。如果对响应速度存在要求，可以使用 GPU 实例进行模型推理（这可能会导致较大的资费消耗）。

</remark>

<disclaimers>

免责声明：   
1. 应用中心仅为您提供应用的逻辑关系，不为您托管任何资源。如果您部署的应用中，存在一定的资源收费现象，请参考对应产品的收费标准；如果您应用所使用的某些产品或者服务因为产品规划等原因发生了不兼容变更，建议您直接咨询对应的产品或者服务；
2. 应用中心为您提供的默认流水线功能是免费的，如果您需要手动切换到自定义流水线可能涉及到资源使用费用，具体的收费标准需要参考函数计算的计费文档；
3. 应用中心部署的部分应用会为您分配“devsapp.cn”的测试域名，这个测试域名并非阿里云官方域名，是 CNCF Sandbox 项目 Serverless Devs 所提供的测试域名，我们不保证该域名的使用时效性，推荐您只在测试的时候使用，或者绑定自己的自定义域名进行使用；
4. 应用部署过程中，如果提示“当前应用模板由社区贡献，非阿里云官方提供，推荐您在使用当前应用模板前仔细阅读应用详情，以确保应用的安全，稳定等”则表示该应用并非阿里云官方所提供的应用，我们仅作为收录和展示，如果您继续部署该应用，推荐您联系应用的作者，并与作者协商应用使用的相关协议等。

</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=fc-mplug-image-captioning) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=fc-mplug-image-captioning) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init fc-mplug-image-captioning -d fc-mplug-image-captioning `
  - 进入项目，并进行项目部署：`cd fc-mplug-image-captioning && s deploy - y`
   
</deploy>

## 应用详情

<appdetail id="flushContent">

### 常见问题

#### 1. 冷启动时间较长如何优化？

因为模型较大，函数计算拉起镜像冷启动时间会比较长，请耐心等待。

#### 2.镜像加速

为了提升冷启动时间，我们提供了镜像加速服务，请关注控制台上的镜像加速状态，只有在 ready 才真正可用。

#### 3 如何自行构建镜像

```bash
IMAGE="registry.cn-hangzhou.aliyuncs.com/aliyun-fc/fc-mplug-image-captioning:v1"
cd src/code/server/
docker build . -t ${IMAGE}
docker push ${IMAGE}
```

</appdetail>

## 使用文档

<usedetail id="flushContent">

### 模型接口

#### 接口描述

|接口描述|Method|Path|参数模式|参数|参数类型|
|:---:|:---:|:---:|:---:|:---:|:---:|
|在线图片描述|**GET**|`/url`|query|url|`string`|
|上传图片描述|**POST**|`/base64`|body|-|`string`|

#### 调用示例

```bash
export endpoint="您在 FC 部署后生成的域名地址"

# 在线图片描述
curl "${endpoint}/url?url=https%3A%2F%2Falice-open.oss-cn-zhangjiakou.aliyuncs.com%2FmPLUG%2Fimage_captioning.png"

# 上传图片描述
curl '${endpoint}/base64' \
  --data-raw "$(base64 -i demo.png)"
  --compressed \
  --insecure

```

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
