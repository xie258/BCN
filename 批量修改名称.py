import xlrd,os,shutil,string  

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import tkinter.messagebox
import tkinter 

def mkdir(filename):
    filepath = str(os.getcwd() )
    folder = os.path.exists(filepath)

    if not folder:
        os.makedirs(filepath)
    else:
        files = open(filepath+str(filename),'w')
        files.close()

import sys
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        filename=str(os.getcwd())+"/"+str(filename)
        self.log = open(filename, 'w')
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass

import time
now=time.strftime("%Y%m%d_%H%M%S", time.localtime())
mkdir('/log/'+str(now)+'_stdout.log')
sys.stdout = Logger('/log/'+str(now)+'_stdout.log', sys.stdout)
sys.stderr = Logger('/log/'+str(now)+'_stderr.log', sys.stderr)

class ExcelData():
    def __init__(self,data_path,sheetname):
        self.data_path = data_path                                 # excle表格路径，传入相对路径
        self.sheetname = sheetname                                 # excle表格内sheet名
        self.data = xlrd.open_workbook(self.data_path)             # 打开excel表格
        self.table = self.data.sheet_by_name(self.sheetname)       # 切换到相应sheet
        self.keys = self.table.row_values(0)                       # 第一行作为key值
        self.rowNum = self.table.nrows                             # 获取表格行数
        self.colNum = self.table.ncols                             # 获取表格列数
        self.faPiaoDaiMa = self.getIndex("发票代码")                #  获取发票代码索引位置
        self.faPiaoHaoMa = self.getIndex("发票号码")                #  获取发票号码索引位置
        print("\n\t－－－－－－－有行row:",self.rowNum)
        print("\t－－－－－－－有列col:",self.colNum)

    # 获取关键字的索引
    def getIndex(self, keyName):
        return self.keys.index(keyName)

## 获取发票pdf的发票代码和发票号码
def splitName(pdfName):
    name=pdfName.split(".")[0]
    return name

## 修改新的名字 根据索引
def getNewName(keyName,addKeyIndex,addSplit):
    ## keyName 关键字列表
    ## *addKeyIndex  添加字段的索引元组
    ## *addSplit     添加对应的字段分隔符元组
    newName=""
    # print(keyName)
    # print(addKeyIndex)
    # print(addSplit)
    length=len(addKeyIndex)  ##字段个数
    for index in range(length):
        if newName=="":
            newName=keyName[addKeyIndex[index]]
            if newName=="":
                return None
        else:
            if keyName[addKeyIndex[index]]=="":
                return None
            newName+=addSplit[index-1]+keyName[addKeyIndex[index]]
    # print(newName)
    return newName

##  根据字段转化为索引
def key_to_index(keyNameChoose,keyNameAll):
    ## keyNameChoose 选择的关键字列表
    ## keyNameAll 所有关键字列表
    transKey=[]  ##转化的索引
    # print(keyNameChoose)
    length=len(keyNameChoose)  ##字段个数
    for index in range(length):
        if keyNameChoose[index] in keyNameAll:
            transKey.append(keyNameAll.index(keyNameChoose[index]))
        else:
            print("%s字段不存在"%keyNameChoose[index])
    # print(transKey)
    return transKey

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

# 读取字段配置文件
def readConfig():
    m_path=os.getcwd()
    con_file=str(os.getcwd())+"/config.txt"
    line=""
    with open(con_file,"r",encoding="utf8") as f:
        try:
            line=f.readline()
        except:
            tkinter.messagebox.showerror('错误','读取'+str(con_file)+'出错了')
            os._exit(0)

    m_choose_key=[]
    m_split_sign=[]
    line=line.split("_")
    length=len(line)
    for index in range(length):
        if index>0:
            m_split_sign.append("_")

        m_choose_key.append(line[index])

    return m_choose_key,m_split_sign

# 全局变量pdf文件夹默认路径
pdf_path=os.getcwd()+"/target"

# 全局变量Excel文件路径
excel_path=os.getcwd()+"/resource/已开票清单模板.xlsx"




# 全局默认字段
# choose_key=["购方企业名称", "发票号码", "产品","开票日期"]
# split_sign=["_","_","_"]
choose_key,split_sign=readConfig()
# print("choose_key:",choose_key)
# print("split_sign:",split_sign)

# 全局变量窗口退出判断
windowState=False

# 正则匹配过滤制定字段
pattern=["饲料有限公司","科技有限公司","贸易有限公司","商务有限公司","饲料科技有限公司","股份有限公司","有限公司","公司",]
pattern=transPattern(pattern)

def go(*args):
    pass

def add(*args):
    if(qk2.cget('text')==""):
        qk2["text"]=qk2["text"]+comboxlist1.get()
        choose_key.append(str(comboxlist1.get()))
    else:
        qk2["text"]=qk2["text"]+comboxlist.get()+comboxlist1.get()
        choose_key.append(str(comboxlist1.get()))
        split_sign.append(str(comboxlist.get()))

def delete(*args):
    if(qk2.cget('text')==""):
        pass
    else:
        qk2["text"]=""
        global choose_key
        global split_sign
        choose_key=[]
        split_sign=[]

def selectPath():
    path_ = askdirectory()
    path.set(path_)   
    ## 绑定全局pdf路径变量
    global pdf_path
    pdf_path=path_

def selectfile():
    filename_ = tkinter.filedialog.askopenfilename()
    # filename_=filename_.replace("/","\\\\")
    filename.set(filename_)
    ## 绑定全局excel路径变量
    global excel_path
    excel_path=filename_

def editFild():
    defaultField["text"]=qk2.cget("text")

def commit():
    win.destroy()

def cancel():
    global windowState
    windowState=tkinter.messagebox.askokcancel('提示','要退出程序吗？')
    if windowState:
        win.destroy()

def on_closing():
    global windowState
    windowState=tkinter.messagebox.askokcancel('提示','确定要退出程序吗？')
    if windowState:
        win.destroy()

if __name__ == '__main__':

    win=tkinter.Tk()
    win.title("批量更改发票名称")
    win.geometry("680x400+300+0")

    path = StringVar()
    path.set(pdf_path) ##默认路径
    filename = StringVar()
    filename.set(excel_path) ##默认文件

    Label(win,text = "PDF文件路径:",padx=25,pady=30).grid(row = 0, column = 0)
    Entry(win, textvariable = path).grid(row = 0, column = 1)
    Button(win, text = "路径选择", command = selectPath).grid(row = 0, column = 2)

    Label(win,text = "EXECL文件:",padx=25,pady=30).grid(row = 0, column = 3)
    Entry(win, textvariable = filename).grid(row = 0, column = 4)
    Button(win, text = "文件选择", command = selectfile).grid(row = 0, column = 5)
    
    Button(win,text = '确定',width=10,height=1,command=commit).place(x=480,y=350)
    Button(win,text = '取消',width=10,height=1,command=cancel).place(x=580,y=350)
    
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()

    if windowState:
        os._exit(0)

    ## 绑定path变量
    # print("excel_path:",excel_path)
    data_path = str(excel_path)
    sheetname = "sheet1"

    # print("excel_path:",excel_path)

    try:
        get_data = ExcelData(data_path,sheetname)
    except:
        tkinter.messagebox.showerror('错误','打开 "'+data_path+'" 出错了')
        os._exit(0)


    choose_index=key_to_index(choose_key,get_data.keys)
    field=getNewName(get_data.keys,choose_index,split_sign)
    if field==None:
        tkinter.messagebox.showerror('错误','读取字段出错了')
        os._exit(0)
    # print(field)

    win=tkinter.Tk()
    win.title("批量更改发票名称")
    win.geometry("680x400+300+0")

    Label(win,text = "默认字段:").place(x=25,y=70)
    defaultField=Label(win,text = field)
    defaultField.place(x=90,y=70)
    # Button(win, text = "修改默认字段", command = editFild).place(x=300,y=70)

    comboxlist2label=Label(win,text="字段：")
    comboxlist2label.place(x=25,y=115)
    comboxlistlabel=Label(win,text="字段分隔符：")
    comboxlistlabel.place(x=245,y=115)

    comvalue1=tkinter.StringVar()
    comboxlist1=ttk.Combobox(win,textvariable=comvalue1)
    # comboxlist1["values"]=("id","name","date")
    ## 绑定Excel 关键字
    comboxlist1["values"]=get_data.keys
    comboxlist1.current(0)
    comboxlist1.bind("<<ComboboxSelected>>",go)
    comboxlist1.place(x=30,y=155)

    comvalue=tkinter.StringVar()
    comboxlist=ttk.Combobox(win,textvariable=comvalue,width=8)
    comboxlist["values"]=("_","#","+",'-','/','.','*')
    comboxlist.current(0)
    comboxlist.bind("<<ComboboxSelected>>",go)
    comboxlist.place(x=250,y=155)

    Button(win,text = '添加',width = 10,height =1,command=add).place(x=400,y=130)
    Button(win,text = '删除',width = 10,height =1,command=delete).place(x=500,y=130)

    qk=Label(win,text="文件名：")
    qk.place(x=30,y=200)
    qk2=Label(win,text=field)
    qk2.place(x=30,y=230)

    Button(win,text = '确定',width=10,height=1,command=commit).place(x=480,y=350)
    Button(win,text = '取消',width=10,height=1,command=cancel).place(x=580,y=350)
    
    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()

    if windowState:
        os._exit(0)

    ## 更新绑定choose_index 值
    choose_index=key_to_index(choose_key,get_data.keys)

    #输入pdf文件目录
    pdfDir = pdf_path

    # pdfDir = "./target"          
        
    #得到pdf目录下的pdf文件名列表  
    files = os.listdir(pdfDir)

    # t = get_data.table.col_values(0, 0, 5)    # 取第1列，第0~5行（不含第5行)
    ## 获取发票号码的列数据
    faPiaoHaoMa_all = get_data.table.col_values(get_data.faPiaoHaoMa,0,get_data.rowNum)
    # print("发票号码:",faPiaoHaoMa_all)
    ## 获取发票代码的列数据
    faPiaoDaiMa_all = get_data.table.col_values(get_data.faPiaoDaiMa,0,get_data.rowNum)
    # print("发票代码:",faPiaoDaiMa_all)

    faPiao_index=[]
    for index in range(len(faPiaoDaiMa_all)):
        # print(str(faPiaoDaiMa_all[index]))
        # print(str(str(faPiaoHaoMa_all[index])))
        faPiao_index.append(str(faPiaoDaiMa_all[index])+'_'+str(faPiaoHaoMa_all[index]))
    # print(faPiao_index)

    # print(files)
    print("\n\n\t－－－－－－－－－－－－－－－－更改记录－－－－－－－－－－－－－－－－\n ")
    for i in files:
        # 如果是目录，跳过
        if os.path.isdir(pdfDir+"/"+i):
            pass
        # 是文件
        else:
            # print(i)
            
            # 获取原pdf名字
            old_name = splitName(i)

            # print("old_name:\n",old_name)

            if old_name in faPiao_index:
                ## 获取所在行
                m_row1=faPiao_index.index(old_name)

                # print(m_row1)


                ## 该发票所在行数据
                m_keys = get_data.table.row_values(m_row1,0,get_data.colNum)

                # 新名
                # choose_key=["购方企业名称", "购方税号","开票日期"]
                # split_sign=["_","_"]
                # print("m_keys:\n",m_keys)
                newName=getNewName(m_keys,choose_index,split_sign)
                if newName==None:
                    tkinter.messagebox.showerror('错误','文件'+newName+'出错了')
                    print("\n\t============================修改异常==============================")
                    print("\t======"+i+"\t文件修改异常！！")
                    print("\t===============================================================\n")
                # print("newname:\n",newName)

                newName = re.sub(pattern,"",str(newName))
                newname = pdfDir +'/'+newName+".pdf"
            else:
                print("\n\t============================没找到==============================")
                print("\t======"+i+"\t文件没找到！！")
                print("\t===============================================================\n")
                continue
            # 更改名字
            old_name=str(pdfDir)+"/"+old_name+".pdf"
            os.rename(old_name, newname)   
            # 输出更改记录
            print("\t旧名字:　 ( %s ) 　－－改为－－　　新名字　( %s )"%(old_name+".pdf",newname) )
    print("\n\n\n\t===============================结束==============================")

    os.system("pause")
