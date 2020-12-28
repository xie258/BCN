const path = require('path');

function resolve (dir) {
  return path.join(__dirname, dir);
}

module.exports = {
  publicPath: './',
  devServer: {
    // can be overwritten by process.env.HOST
    host: '0.0.0.0',  
    port: 8080
  },
  // 路径缩写定义
  chainWebpack: config => {
    config.resolve.alias
      .set('@', resolve('src'))
      .set('src', resolve('src'))
      .set('common', resolve('src/common'))
      .set('components', resolve('src/components'));
  },
  // 打包配置
  pluginOptions: {
      electronBuilder: {
          builderOptions: {
            "productName":"BO",//项目名，也是生成的安装文件名，即aDemo.exe
            "copyright":"Copyright © 2020",//版权信息
            // "directories":{
            //     "output":"./dist"//输出文件路径
            // },
            "win":{//win相关配置
                "icon":"./public/app.ico",//图标，当前图标在根目录下，注意这里有两个坑
                "target": [
                    {
                        "target": "nsis",//利用nsis制作安装程序
                        "arch": [
                            "x64"  //64位
                        ]
                    }
                ]
            },
            "asar":false,   //不压缩
            "nsis": {
              "oneClick": false, // 是否一键安装
              "allowElevation": true, // 允许请求提升。 如果为false，则用户必须使用提升的权限重新启动安装程序。
              "allowToChangeInstallationDirectory": true, // 允许修改安装目录
              "installerIcon": "./public/app.ico",// 安装图标
              "uninstallerIcon": "./public/app.ico",//卸载图标
              "installerHeaderIcon": "./public/app.ico", // 安装时头部图标
              "createDesktopShortcut": true, // 创建桌面图标
              "createStartMenuShortcut": true,// 创建开始菜单图标
              "shortcutName": "BO", // 图标名称
          },
          }
      }
  }
};
