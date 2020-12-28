from flask import Flask, request, json , jsonify
# 开启多线程
import pythoncom

# from multiprocessing import Process



import time,datetime

# 正则匹配
import re

import os
import sys 
from win32com.client import DispatchEx

from concurrent.futures import ThreadPoolExecutor

## 启动线程
executor = ThreadPoolExecutor(2)

app = Flask(__name__)

# server = Process(target=app.run(host="0.0.0.0", port=8088, debug=False))

# 获取当前路径
pwd = os.getcwd()

# excel表名称
excelName = "批量做合同单模板.xlsx"

# excel文件位置
excelLocation = os.path.join(pwd , excelName)

# pdf 导出路径
exportDir = os.path.join(pwd, 'PDF')

# 需要打印的合同模板
# templateList = ["清远酸动力合同","广东绿生源合同", "上海酸能埃赛合同"]
templateList = {"Q":"清远酸动力合同","G":"广东绿生源合同", "S":"上海酸能埃赛合同"}
templateListChoose = ["Q","G"]

# 提供的分隔符
separator = ["_","+","*","-","/","#","."]

# 用户选择的分隔符
separatorChoose = [1]

# 打开excel对象
xlApp = None

# excelbooks对象
books = None

# 选择的字段
fieldChoose = [2,4]
field = []

# 添加企业简称字段
complexCompany = "客户"
simpleCompany = "企业简称"

# 保存日志
log_respone = []
start = 0
end = 0
now = 0

complete = 0

# 线程停止标志
stop = False

# excel打开标志锁
excelLock = False

## 正则匹配patter格式转换
def transPattern(list_pattern):
    length = len(list_pattern)
    pat="("
    for index in range(length):
        if index==0:
            pat+=str(list_pattern[index])
        else:
            pat+="|"+str(list_pattern[index])
    pat+=")"
    # print("pat:",pat)
    return pat

# 过滤字段
pattern=["饲料有限公司","科技有限公司","贸易有限公司","商务有限公司","饲料科技有限公司","股份有限公司","有限公司","公司",]
pattern = transPattern(pattern)


def jianCheng():
    try:
        global excelLock

        # 获取锁
        while excelLock == True:
            time.sleep(3)


        excelLock = True

        # 启动线程
        pythoncom.CoInitialize()

        # 打开excel
        global xlApp
        xlApp = DispatchEx("Excel.Application")
        xlApp.Visible =False
        xlApp.DisplayAlerts = 0

        # 指定工作簿
        global books
        books = xlApp.Workbooks.Open(excelLocation,False)
        sheet = books.Worksheets("订货记录")



        # 测试
        # st = books.Worksheets("订货记录").Cells(10,3).Value
        # date2str = str(books.Worksheets("订货记录").Cells(10,3).Value).rstrip("+00:00")
        # print(date2str)
        # # print(datetime.datetime.strptime(date2str, '%Y-%m-%d %H:%M:%S'))
        # print(st.datetime.strptime(date2str, '%Y-%m-%d %H:%M:%S'))
        # # date2str = datetime.datetime.strptime(date2str, '%Y-%m-%d')
        # print(st)
        # print(date2str)
        # mig = date2str + "nihaoma"
        # print(mig)

        # try:
        #     # sl = datetime.datetime.strptime("2016-04-01 17:29:25+00:00".rstrip("+00:00"), '%Y-%m-%d %H:%M:%S')
        #     s1 = "2016-04-01 00:00:00+00:00"
        #     # s1 = datetime.datetime.strptime(s1.replace(" 00:00:00+00:00",""), '%Y-%m-%d')
        #     dt = datetime.datetime.strptime(s1.replace(" 00:00:00+00:00",""), '%Y-%m-%d')
        #     s1 = dt.strftime("%Y-%m-%d")
        #     print(s1)
        #     mig = s1 + "sldkjflsdf"
        #     print(mig)
        #     s2 = datetime.datetime(2016, 4, 1, 17, 29, 25)
        #     print(s2)
        #     print("succes")
        # except:
        #     print("error")

        # print("xlapp:",xlApp)
        # print("boks:",books)

        # 获取订货记录行和列
        row = sheet.UsedRange.Rows.Count
        col = sheet.UsedRange.Columns.Count

        for i in range(7,row):
            # print(complexCompany)
            # print(books.Worksheets("订货记录").Cells(i,field.index(complexCompany)+1).Value)
            allName = books.Worksheets("订货记录").Cells(i,field.index(complexCompany)+1).Value
            # print(allName)
            if(allName is None):
                continue
            subName = re.sub(pattern,"",str(allName))
            # print(subName)
            # print(field.index(simpleCompany)+1)
            # print(field)
            # print( books.Worksheets("订货记录").Cells(i,field.index(simpleCompany)+1).Value)
            books.Worksheets("订货记录").Cells(i,field.index(simpleCompany)+1).Value = subName
        
            # 关闭程序
        books.Close(True)
        xlApp.Quit()
        del(xlApp)

        # 释放资源
        pythoncom.CoUninitialize()
        # print("修改简称完毕")

        # 释放锁
        excelLock = False

        xlApp = None
    except:
        return None
        # print("程序转化简称异常错误")

# 打印函数
def convert():

    
    global excelLock
    # 获取锁
    while excelLock == True:
        time.sleep(3)

    excelLock = True

      # 启动线程
    pythoncom.CoInitialize()

    # 打开excel
    global xlApp
    xlApp = DispatchEx("Excel.Application")
    xlApp.Visible =False
    xlApp.DisplayAlerts = 0



    # 指定工作簿
    global books
    books = xlApp.Workbooks.Open(excelLocation,False)
    sheet = books.Worksheets("订货记录")

    # 获取订货记录行和列
    row = sheet.UsedRange.Rows.Count
    col = sheet.UsedRange.Columns.Count

    global now
    now = 0

    global start
    start = 0

    global end
    end = 0

    global complete
    complete = 0


    # # 关闭程序
    # books.Close(True)

    # xlApp.Quit()
    # del(xlApp)
    #     # 释放资源
    # pythoncom.CoUninitialize()
    global log_respone
    log_respone = []

    log_respone.append("#####################    程序已开始    #####################")
    
    for i in range(7,row):
        
        if(stop):
            now += 1
            # print("项目已停止")
            log_respone.append("#####################    程序已结束    #####################")
            complete = 1
            # print(log_respone)
            break

    #   # 启动线程
    #     pythoncom.CoInitialize()
    #     xlApp = DispatchEx("Excel.Application")
    #     xlApp.Visible =False
    #     xlApp.DisplayAlerts = 0
        
        books = xlApp.Workbooks.Open(excelLocation,False)

        # 修改合同单号
       
        contractId = books.Worksheets("订货记录").Cells(i,2).Value
        print(contractId)

        if(contractId[0] in templateListChoose):
            templateName = templateList[contractId[0]]
        else:
            continue

        books.Worksheets(templateName).Cells(4,10).Value  = books.Worksheets("订货记录").Cells(i,2).Value

        # 打印PDF文件名
        exportName = ''
        for index,value in enumerate(fieldChoose):
            if(index>0 and exportName!=''):     
                if(books.Worksheets("订货记录").Cells(i,value).Value is None):
                    continue
                exportName += str(separator[separatorChoose[index-1]-1])
                # print(books.Worksheets("订货记录").Cells(i,value).Value)
                # print(type(books.Worksheets("订货记录").Cells(i,value).Value))
                try:
                    if value == 3:
                        date2str = str(books.Worksheets("订货记录").Cells(i,value).Value)
                        # print(date2str)
                        date2str = datetime.datetime.strptime(date2str.replace(" 00:00:00+00:00",""), '%Y-%m-%d')
                        # print(date2str)
                        date2str = date2str.strftime("%Y-%m-%d")
                        # print(date2str)
                        exportName += str(date2str)
                    else:
                        exportName += str(books.Worksheets("订货记录").Cells(i,value).Value)
                except:
                    continue
            else:
                if(books.Worksheets("订货记录").Cells(i,value).Value is None):
                    continue
                # print(books.Worksheets("订货记录").Cells(i,value).Value)
                # print(type(books.Worksheets("订货记录").Cells(i,value).Value))
                try:
                    if value == 3:
                        date2str = str(books.Worksheets("订货记录").Cells(i,value).Value)
                        # print(date2str)
                        date2str = datetime.datetime.strptime(date2str.replace(" 00:00:00+00:00",""), '%Y-%m-%d')
                        # print(date2str)
                        date2str = date2str.strftime("%Y-%m-%d")
                        # print(date2str)
                        exportName += str(date2str)
                    else:
                        exportName += str(books.Worksheets("订货记录").Cells(i,value).Value)
                except:
                    continue

        exportName += '.pdf'


        templateFolder = os.path.join(pwd,str(templateName))
        # print(templateFolder)
        # print(os.path.exists(templateFolder))
        if os.path.exists(templateFolder) == False:
            # print("创建目录")
            os.makedirs(templateFolder)

        
        export = os.path.join(templateFolder,exportName)
        # print(export)
        if os.path.isfile(export):
            # print("文件 %s  未打印，存在相同文件名\n" % export)
            log_respone.append("文件 %s  未打印，存在相同文件名\n" % exportName)
            now += 1
            # print("print  now:", now)
            continue
        # books.Worksheets("广东绿生源合同").ExportAsFixedFormat(0,export)

        try:
            books.Worksheets(templateName).ExportAsFixedFormat(0,export)
            # print('文件:', exportName)
            
            # 保存日志记录
            log_respone.append("已生成  %s  文件\n" % export)
            # print(log_respone)

            # print(log_respone)
        except:
            # print('文件:', exportName)
            
            # 保存日志记录
            log_respone.append("文件 %s  改名失败\n" % export)

        # print(log_respone)
        now += 1

        # print("print  now:", now)


        # # 关闭程序
        # books.Close(True)

        # xlApp.Quit()
        # del(xlApp)
        #     # 释放资源
        # pythoncom.CoUninitialize()

        # 关闭程序

    # now += 1
    books.Close(True)

    xlApp.Quit()
    del(xlApp)
        # 释放资源
    pythoncom.CoUninitialize()

    xlApp = None
    # print("程序结束")

    complete = 1

        # 释放锁
    excelLock = False


## 整合excel路径和合同模板
@app.route('/postInformation', methods = ['POST', 'GET'])
def postInformation():
    if request.data:
        try:
            data = json.loads(request.data)
            global excelLocation
            excelLocation = data["excel"]
            # print(excelLocation)
        except:
            return "请求excel文件参数错误",400

        try:
            global templateListChoose
            templateListChoose = data["templateList"]
            # print(templateListChoose)
        except:
            return "请求合同参数错误",400


        # print(excelLocation)
        # 启动线程
        pythoncom.CoInitialize()

        # 打开excel程序
        global xlApp
        xlApp = DispatchEx("Excel.Application")
        xlApp.Visible =False
        xlApp.DisplayAlerts = 0

        # 指定工作簿
        global books
        try:
            books = xlApp.Workbooks.Open(excelLocation,False)
            sheet = books.Worksheets("订货记录")

            # 获取订货记录行和列
            row = sheet.UsedRange.Rows.Count
            col = sheet.UsedRange.Columns.Count

            books.Worksheets("广东绿生源合同").Cells(4,10).Value

            # 获取字段
            global field
            field = sheet.Range(sheet.Cells(6,1),sheet.Cells(6,col)).Value
            field = list(list(field)[0])

            if( simpleCompany not in field):
                books.Worksheets("订货记录").Cells(6,col+1).Value = simpleCompany
                field.append(simpleCompany)
            
            # 过滤字段
            if(complexCompany not in field ):
                books.Close(False)
                xlApp.Quit()
                del(xlApp)

                # 释放资源
                pythoncom.CoUninitialize()
                return "找不到用于过滤的用户名"
            
            # 关闭程序
            books.Close(True)
            xlApp.Quit()
            del(xlApp)

            # 释放资源
            pythoncom.CoUninitialize()

            # 异步执行更新简要名称
            executor.submit(jianCheng)
        except:
            # print("打开%s错误" % excelLocation)
            return "打开%s错误"%excelLocation,400

        response = jsonify({'field': field,'separator': separator})
        return response, 200

        return "获取参数成功",200
    else:
        return "请求参数错误",400

# 修改excel 路径
@app.route('/postPath', methods = ['POST', 'GET'])
def postPath():
    if (request.data):
        data = json.loads(request.data)
        global excelLocation
        excelLocation = data["excel"]
        # print(excelLocation)
        return "获取参数成功",200
    else:
        return "请求参数错误",400

# 修改templateList 合同模板
@app.route('/postTemplate', methods = ['POST', 'GET'])
def postTemplate():
    if (request.data):
        data = json.loads(request.data)
        global templateListChoose
        # print(data)
        templateListChoose = data["templateList"]
        # print(templateListChoose)
        return "获取参数成功",200
    else:
        return "请求参数错误",400

@app.route('/getFieldAndSeparator', methods = ['POST', 'GET'])
def getFieldAndSeparator():

    # print(excelLocation)
    # 启动线程
    pythoncom.CoInitialize()

    # 打开excel程序
    global xlApp
    xlApp = DispatchEx("Excel.Application")
    xlApp.Visible =False
    xlApp.DisplayAlerts = 0

    # 指定工作簿
    global books
    try:
        books = xlApp.Workbooks.Open(excelLocation,False)
        sheet = books.Worksheets("订货记录")

        # 获取订货记录行和列
        row = sheet.UsedRange.Rows.Count
        col = sheet.UsedRange.Columns.Count

        books.Worksheets("广东绿生源合同").Cells(4,10).Value

        # 获取字段
        global field
        field = sheet.Range(sheet.Cells(6,1),sheet.Cells(6,col)).Value
        field = list(list(field)[0])

        if( simpleCompany not in field):
            books.Worksheets("订货记录").Cells(6,col+1).Value = simpleCompany
            field.append(simpleCompany)
        
        # 过滤字段
        if(complexCompany not in field ):
            books.Close(False)
            xlApp.Quit()
            del(xlApp)

            # 释放资源
            pythoncom.CoUninitialize()
            return "找不到用于过滤的用户名"
        
        # 关闭程序
        books.Close(True)
        xlApp.Quit()
        del(xlApp)

        # 释放资源
        pythoncom.CoUninitialize()

        # 异步执行更新简要名称
        executor.submit(jianCheng)
    except:
        # print("打开%s错误" % excelLocation)
        return "打开%s错误"%excelLocation,400

    response = jsonify({'field': field,'separator': separator})
    return response, 200

@app.route('/printContract', methods = ['POST', 'GET'])
def printContract():

    if (request.data):
        data = json.loads(request.data)
        global fieldChoose
        fieldChoose = data["fieldChoose"]
        # print(fieldChoose)

        global separatorChoose
        separatorChoose = data["separatorChoose"]
        # print(separatorChoose)
    else:
        return "请求参数错误",400

    global stop
    stop = False

    global complete
    complete = 0


    executor.submit(convert)
    # print("已启动打印程序")
    return "已启动打印程序",200

@app.route('/getLog', methods = ['POST', 'GET'])
def getLog():
    global start
    global end
    global log_respone
    start = end

    # print("now:",now)
    # print("end:",end)
    # print("complete:",complete)
    for i in range(5):
        if(end<=now):
            # if(log_respone):
            #     log_respone=[]
            #     print("日志已结束")
            #     return "程序已结束1",200
            end += 1
        else:
            if(complete == 1 and end==start):
                # print("程序已结束")
                return "程序已结束",200
            # else:
            #     return "暂时没有数据1",200

    
    m_response = log_respone[start:end]
    if(m_response):
        m_response = jsonify({'log': m_response})
        # print(m_response)
    else:
        return "暂时没有数据",200

    return m_response,200

@app.route('/stopPrint', methods = ['POST', 'GET'])
def stopPrint():
    global stop
    stop = True

    # global start
    # start = 0
    
    # global end
    # end = 0

    global complete
    complete = 1

    # log_respone = []

    # global xlApp
    # if xlApp is not None:
    #     del(xlApp)

    # 释放资源
    pythoncom.CoUninitialize()
        
    # print("已停止程序......")
    return "停止",200


def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/kill', methods = ['POST', 'GET'])
def kill():

    global stop
    stop = True

    global complete
    complete = 1

    # 释放资源
    pythoncom.CoUninitialize()
    shutdown()
    # os._exit(0)
    # global server
    # server.terminate()
    return "杀死进程",200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088, debug=False)
    # server.start()
    # server.join()