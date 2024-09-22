
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

FC多集群调度解决方案(fc3.0)

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
| 函数计算 |  AliyunFCFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |
| OTS |  AliyunOTSFullAccess | [帮助文档](https://help.aliyun.com/zh/tablestore/product-overview/) [计费文档](https://help.aliyun.com/zh/tablestore/product-overview/billing-overview) |


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

### 背景

大客户通常会在专有云等环境自持一部分 GPU 资源，同时也使用公有云 GPU 资源，实现更低的成本。这种混合的资源模式，会面临两个主要的挑战：
1. 自持的 GPU 资源普遍负载不均，利用率低。尤其在在线应用场景下，流量波动，这个问题更严重。
2. 没有一套完整的混合调度方案，能够优先充分使用自持 GPU 的资源，并且在自持资源不够时，能及时的调度 FC GPU 等全托管的 GPU 算力进行处理。

针对以上挑战，我们设计了一套 GPU 流量混合调度方案。在深入方案细节之前，我们先详细分析上述两个挑战。

#### 挑战1：自持 GPU 集群负载不均，资源利用率低

对于典型的 GPU 集群，在执行推理请求，尤其是在线推理请求时，通常会因为如下原因，导致请求耗时出现毛刺，GPU 卡负载不均。

* 卡型差异（硬件造成的推理耗时差异）：同一模型运行在同一个推理endpoint，但使用不同GPU（V100、T4等）
* 模型差异（模型造成的推理耗时差异）：不同模型运行在同一个推理endpoint，比如机器翻译的多语言（zh->cn、jp->cn）
* 输入差异（输入造成的推理耗时差异）：同一模型运行在同一个推理endpoint，但不同请求输入造成模型推理耗时差异，比如GPT

传统的 Round-Robin 等负载均衡算法在这样的场景下，效果并不好。请求毛刺多，GPU 负载不均。下图是对运行在5个 GPU 实例上的 Gemma-2b 模型推理服务的测试。结果如下：

<img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/sched_1.png?raw=true" width=500 />

从“响应时长”图中可以看到，同时发送3-5个推理请求时，此时并未超过整个集群5个实例的处理能力，但是由于实例负载不均，此时请求延时已经出现很多毛刺。下图是5个实例的 GPU 利用率，可以看到利用率波动较大，负载不均。

<img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/sched_2.png?raw=true" width=500 />

#### 挑战2：实现一套完整的支持混合 GPU 资源环境的请求流量调度方案

<img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/sched_3.png?raw=true" width=500 />


上述流量调度的关键是要能准确判断 “IDC 自持 GPU” 处理能力是否已经饱和，当前的网关不具备这样的能力。例如通常网关支持按比例调度流量到不同的后端服务。在上述场景下，自持 GPU 集群处理是否饱和，受请求输入，GPU 卡型/数量，模型等多种因素影响，很难用一个静态的值衡量。而且这个比例需要随着集群扩缩容而及时更新，运维复杂度很高。


### 解决方案概述
<img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/sched_4.png?raw=true" width=500 />

如上图所示，该解决方案的关键是在自持 GPU 算力前面引入 FC 函数，其中 FC 实例和自持 GPU 的实例是 1:1 的，换句话说，FC 实例是 自持 GPU 实例的“化身”。FC 系统调度 FC 实例就间接调度了 GPU 实例。

FC 系统将追踪所有实例处理请求的状态，例如哪些实例正在处理请求，哪些空闲，然后将请求分配给空闲实例。这套流量调度机制能够保证：
1. 所有的 FC 实例是负载均衡的。如果有实例空闲，那么立即会被分配请求。
2. 如果设置了函数的实例上限，当没有实例能处理新的请求时，会立即返回 429 流控错误。
因此能很好的满足 GPU 混合算力调度的需求。


</appdetail>

## 使用流程

<usedetail id="flushContent">

### OTS初始化

基于FC的多集群调度解决方案依赖OTS（表格存储）进行元信息数据持久化，使用前需要开通并初始化OTS。

1. OTS实例规格与表结构如下：

- OTS实例：
  - 实例名称：fc-sched
  - 规格：高性能型
- OTS表：
  - 表名称：endpoints
  - 数据生命周期：-1（永不过期）
  - 最大版本数：1（不启用多版本）
  - 主键与属性：如下

| 字段类型    | 字段名称   | 字段数据类型 | 字段说明 |
| ---------- | -------- | ---------- | ------- |
| PrimaryKey | endpoint | String     | 存储用户自建IDC集群的各GPU POD服务地址 |
| Attribute  | ref      | Integer    | endpoint引用计数，当前仅0/1（未分配/已分配）|
| Attribute  | last_update_tms | Integer | endpoint最近一次的保活更新时间 |

2. OTS实例规格与表结构初始化，可参考如下操作：

step1: 创建OTS数据库、并开放公网访问

 <img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/ots_1.png?raw=true" width=300 />

step2: 创建OTS数据表、以及初始化该表主键

 <img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/ots_2.png?raw=true" width=300 />

### FC部署

通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署该解决方案：
- [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
- 初始化项目：`s init fc3-sched -d fc3-sched`
- 进入项目，并进行项目部署：`cd fc3-sched && s deploy -y`

完成部署后，可以通过FC控制台查看已部署的FC函数，分别作用如下：
- fc-sched-{namespace-id}-ops : 运维管控函数（控制面）
  - 提供访问端点（公网、内网），admin通过该访问端点访问运维管控函数、并进行运维管控操作
  - 控制面操作：增加、删除、查看用户自建IDC的后端GPU节点
- fc-sched-{namespace-id}-core : 请求转发函数（数据面）
  - 提供访问端点（公网、内网），将推理请求转发至用户自建IDC GPU集群
  - 数据面功能：将推理请求转发至用户自建IDC的后端GPU节点
- fc-sched-{namespace-id}-proxy : 网关函数
  - 内置nginx转发调度策略，优先将推理请求调度至用户自建IDC集群，并当用户自建IDC集群工作饱和后（429），将推理请求重试至用户云上FC集群。

如下两图展示了部署后的FC函数、以及不同函数的访问endpoint。
  
 - <img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/sched_5.png?raw=true" width=300 />
 - <img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/sched_6.png?raw=true" width=300 />

 用户需要对部署后的FC函数进行更新，以便控制转发策略、满足可观测等需求。

 - fc-sched-proxy : 网关函数
   - 修改nginx upstream配置：
     - primary upstream：指定为fc-sched-{namespace-id}-core函数的访问端点，优先将推理请求调度至用户自建IDC集群。
     - backup upstream：指定为用户云上FC集群的访问端点，当primary upstream出现429、5xx、timeout时将重试推理请求至该backup集群；需要将用户自建IDC集群提供的推理服务，在云上FC集群复建；对于典型的SD应用可快速通过FC应用中心提供的应用模板进行复建。
       - SD应用模板：[链接](https://fcnext.console.aliyun.com/applications/ai/create?template=29)
       - SD应用模板说明：[链接](https://alidocs.dingtalk.com/i/p/x9JOGOjr65om4QLAdy0mV8B0gpkodz89?spm=5176.fcnext.0.0.7bea78c8O7OYOn)
   - <img src="https://github.com/devsapp/start-fc-gpu/blob/v3/materials/sched_7.png?raw=true" width=300 />

- fc-sched-core : 转发函数
  - **开启VPC配置**，以便可通过VPC将推理请求转发至用户自建IDC集群的GPU Endpoint。

- 所有函数：
  - 开启函数日志功能。

**注意**：对函数进行任何修改后，请进入项目并重新项目部署：`cd fc3-sched && s deploy -y`，以便修改生效；或者可以直接在FC控制台进行修改以便生效。

### 注册用户自建IDC集群的GPU Endpoint

假定用户自建IDC集群暴露了192.168.10.10:7860、192.168.10.11:7860后端GPU Endpint（VPC内可访问），可通过如下命令对如上2个GPUEndpoint进行注册：

* curl -v "http://your-fc-sched-ops-endpoint/endpoint/register?endpoint=192.168.10.10:7860"
* curl -v "http://your-fc-sched-ops-endpoint/endpoint/register?endpoint=192.168.10.11:7860"

### 测试转发功能

#### 测试推理请求是否可正常转发至用户自建IDC集群（primary upstream）

* 发送推理请求至fc-sched-core的公网访问URL。
* 对于SD API，可修改`test/test.py`中的endpoint，并执行测试。

#### 测试推理请求是否可正常转发至用户云上FC集群（backup upstream）

* 发送推理请求至用户云上FC函数的公网访问URL。
* 对于SD API，可修改`test/test.py`中的endpoint，并执行测试。

#### 测试推理请求是否可在多集群进行转发：优先用户自建IDC集群，次之用户云上IDC集群

* 假定fc-sched-ops/core已代管用户自建推理服务的2个GPU IP，该集群并发处理能力上限为2
* 发送推理请求到fc-sched-proxy的公网访问URL
    * 并发1：推理请求转发至primary upstream
    * 并发2：推理请求转发至primary upstream
    * 并发3：2个推理请求转发至primary upstream，超出用户自建IDC集群的并发处理后，额外的1个请求被转发至backup upstream

</usedetail>


### 运维管控接口：

fc-sched-ops函数提供了如下运维管控接口，用以代管用户自建IDC集群

* 注册后端GPU Ednpoint:
   * METHOD: GET
   * PATH: /endpoint/register?endpoint=ip[:port]
   * 说明：注册成功后，fc-sched-ops会自动调整fc-sched-core转发函数的实例数量，以保证转发实例与后端GPU实例的一一对应关系。
* 取消注册后端GPU Endpoint:
   * METHOD: GET
   * PATH: /endpoint/unregister?endpoint=ip[:port]
   * 说明：取消注册成功后，fc-sched-ops会自动调整fc-sched-core转发函数的实例数量，以保证转发实例与后端GPU实例的一一对应关系。
* 查看所有已注册的后端GPU Endpoint状态：
   * METHOD: GET
   * PATH: /endpoint/list


## 注意事项

<matters id="flushContent">

- FC函数权限: 
  - fc-sched-[core|ops]函数角色可使用默认的aliyunfcdefaultrole, 并为aliyunfcdefaultrole增加AliyunOTSFullAccess,AliyunOTSWriteOnlyAccess
,AliyunOTSReadOnlyAccess权限。

- OTSEndpoint: 
  - 需要为OTSEndpint开启公网访问权限、或VPC访问权限; 当OTSEndpint开启VPC访问权限时, 请为fc-sched-[core|ops]配置相同的VPC。

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
