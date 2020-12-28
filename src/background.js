'use strict'

import { app, protocol, BrowserWindow , globalShortcut, Menu} from 'electron'
// import { app, protocol, BrowserWindow , Menu ,ipcMain,globalShortcut} from 'electron'
import {
  createProtocol
} from 'vue-cli-plugin-electron-builder/lib'

const isDevelopment = process.env.NODE_ENV !== 'production'

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win

let serverProcess

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([{
  scheme: 'app',
  privileges: {
    secure: true,
    standard: true
  }
}])

function createWindow () {
  // Create the browser window.
  win = new BrowserWindow({
    width: 1122,
    height: 737,
    minWidth:1020,
    minHeight:670,
    frame:false,
    webPreferences: {
      webSecurity: false,
      nodeIntegration: true
    },
		webContents: {
		  openDevTools: true   //不想要控制台直接把这段删除
		},
    icon: `${__static}/app.ico`
  })

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }

  win.on('closed', () => {
    win = null
  })
  createMenu()
}

// 从 python-shell 导入一个 PythonShell 对象 (注意大小写)
// const {PythonShell}  = require("python-shell")
// PythonShell 主要有 run() 和 runString() 两个方法, 这里我们用 run()
// run() 第一个参数是要调用的 py 文件的路径
// 第二个参数是可选配置 (一般传 null)
// 第三个参数是回调函数
// PythonShell.run(
// 	"service.exe", null, function (err, results) {
//         if (err) throw err
//         console.log('results', results)
//     }
// )


// 设置菜单栏
function createMenu() {
    // darwin表示macOS，针对macOS的设置
    if (process.platform === 'darwin') {
        const template = [
        {
            label: 'App Demo',
            submenu: [
                {
                    role: 'about'
                },
                {
                    role: 'quit'
                }]
        }]
        let menu = Menu.buildFromTemplate(template)
        Menu.setApplicationMenu(menu)
    } else {
        // windows及linux系统
        Menu.setApplicationMenu(null)
    }
}


// ipcMain.on('message',(event,data)=>{
//   console.log(data);  //通过控制台打印渲染进程发送来的消息
// })


// 启动后台服务进程
const exec = require('child_process').exec

// 本地后台服务名称路径
// let cmdStr = 'service.exe'
// let serverPath=`${__static}`

// serverProcess=require('child_process').spawn(cmdStr,{cwd:serverPath})


// const exec = require('child_process').exec

// 任何你期望执行的cmd命令，ls都可以
let cmdStr = 'service.exe'
// 执行cmd命令的目录，如果使用cd xx && 上面的命令，这种将会无法正常退出子进程
// let cmdPath = `${__static}` 
// 子进程名称
let workerProcess

function runExec() {
  // 执行命令行，如果命令不需要路径，或就是项目根目录，则不需要cwd参数：
  // workerProcess = exec(cmdStr, {cwd: cmdPath})
  workerProcess = exec(cmdStr, {})
  // 不受child_process默认的缓冲区大小的使用方法，没参数也要写上{}：workerProcess = exec(cmdStr, {})

  // 打印正常的后台可执行程序输出
  workerProcess.stdout.on('data', function (data) {
    console.log('stdout: ' + data);
  });

  // 打印错误的后台可执行程序输出
  workerProcess.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
  });

  // 退出之后的输出
  workerProcess.on('close', function (code) {
    console.log('out code：' + code);
  })
}

// runExec()

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  runExec()
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    // try {
    //   await installVueDevtools()
    // } catch (e) {
    //   console.error('Vue Devtools failed to install:', e.toString())
    // }
  }
	globalShortcut.register('CommandOrControl+Shift+i', function () {
	  win.webContents.openDevTools()
	})
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', data => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
