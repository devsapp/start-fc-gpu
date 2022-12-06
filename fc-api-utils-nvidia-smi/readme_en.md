# Application development instructions

<p align="center"><b> <a href="./readme.md"> 中文 </a> | English </b></p>

> The development of Serverless Devs applications must strictly conform to the [application model specification](../../spec/en/0.0.2/serverless_package_model/3.package_model.md#Application-model-specification) in [Serverless Package Model](../../spec/en/0.0.2/serverless_package_model/readme.md). In the [application model specification](../../spec/en/0.0.2/serverless_package_model/3.package_model.md#Application-model-specification), the instructions on [application model metadata](../../spec/en/0.0.2/serverless_package_model/3.package_model.md#Application-model-metadata) are described. 

The component development cases of Serverless Devs are integrated into the Serverless Devs CLI tool. You can use the CLI tool to initialize an application project that is not developed. Developers only need to run the s init command, and the following command output is returned:

```shell script

🚀 Serverless Awesome: https://github.com/Serverless-Devs/package-awesome

? Hello Serverless for Cloud Vendors (Use arrow keys or type to search)
❯ Alibaba Cloud Serverless 
  AWS Cloud Serverless 
  Tencent Cloud Serverless 
  Baidu Cloud Serverless 
  Dev Template for Serverless Devs 
```

Select the last line `Dev Template for Serverless Devs` and press the Enter key. The following command output is returned: 


```shell script
$ s init

🚀 Serverless Awesome: https://github.com/Serverless-Devs/package-awesome

? Hello Serverless for Cloud Vendors Dev Template for Serverless Devs
? Please select an Serverless-Devs Application (Use arrow keys or type to search)
❯ Application Scaffolding 
  Component Scaffolding 
```

Select the `Application Scaffolding` and press the Enter key. The project of a Serverless Devs application is initialized. You can view the file tree by using the following command:

```shell script
$ find . -print | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
.
|____readme.md
|____version.md
|____publish.yaml
|____src
| |____s.yaml
| |____index.js
```

The following table describes the directories in the file tree: 

| Directory    | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| readme.md    | Description of the component, or help  documentations.       |
| version.md   | The description of the project version,  such as the updates of the current version. |
| publish.yaml | The file that is a required for the  project. The file is identifiable for developers of Serverless Devs Package. |
| src          | The directory where the application is  located, which needs to include s.yaml and related application code. |


Developers can develop applications by using the code stored in the src directory and write the `publish.yaml` file for the project. After the preceding operations are complete, you can commit the project to different sources. For example, if you want to commit the project to GitHub Registry, you can create a repository named `Public` in GitHub, store the compiled code into the repository, and then publish a version. In this case, the application is available on Serverless Devs clients.