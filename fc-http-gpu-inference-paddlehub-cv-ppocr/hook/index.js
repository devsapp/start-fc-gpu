async function preInit(inputObj) {
    console.log(`
    ╭━━━┳━━━╮╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╭╮╱╱╱╱╱╱╱╱╱╱╭━━━┳━━━┳╮╱╭╮
    ┃╭━━┫╭━╮┃┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱╱╱┃╭━╮┃╭━╮┃┃╱┃┃
    ┃╰━━┫┃╱╰╯┃╰━━┳━━┳━┳╮╭┳━━┳━┫┃╭━━┳━━┳━━╮┃┃╱╰┫╰━╯┃┃╱┃┃
    ┃╭━━┫┃╱╭╮╰━━╮┃┃━┫╭┫╰╯┃┃━┫╭┫┃┃┃━┫━━┫━━┫┃┃╭━┫╭━━┫┃╱┃┃
    ┃┃╱╱┃╰━╯┃┃╰━╯┃┃━┫┃╰╮╭┫┃━┫┃┃╰┫┃━╋━━┣━━┃┃╰┻━┃┃╱╱┃╰━╯┃
    ╰╯╱╱╰━━━╯╰━━━┻━━┻╯╱╰╯╰━━┻╯╰━┻━━┻━━┻━━╯╰━━━┻╯╱╱╰━━━╯

    * Welcome to FC Serverless GPU
    - Code : https://github.com/devsapp/start-fc-gpu
    - Manual : https://help.aliyun.com/document_detail/56417.html
    
    * Cloud services required：
    - FC : https://fc.console.aliyun.com/
    - ACR: https://cr.console.aliyun.com/

    * Tips：
    - FC Component: https://www.serverless-devs.com/fc/readme
    `)
}

async function postInit(inputObj) {
    console.log(`
    * Before using, please check whether the actions command in Yaml file is available
    * Carefully reading the notes in s.yaml is helpful for the use of the tool
    * If need help in the use process, please apply to join the Dingtalk Group: 33947367
    `)
}

module.exports = {
    postInit,
    preInit
}
