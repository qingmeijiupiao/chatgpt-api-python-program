from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui import Ui_ChatBot # 从ui文件中导入类
import openai

import json

with open("promot_setting.json",encoding="utf-8") as promot_setting:
# 读取json数据
    promot = json.load(promot_setting)

#默认角色
character = "人"

#创建消息数组
aimessage=[]
aimessage.append(
    {"role": "user", "content":promot[0]}
    )
#api key 默认,发布时记得注释掉
key = ""


#设置apikey函数
def set_apikey(key):
    if len(key) == 51:
        openai.api_key=key
        return True
    else:
        return False
set_apikey(key)
# 定义一个函数get_answer，输入消息给api返回回答
def get_answer(message):
    global key
    #判断是否输入了apikey
    if set_apikey(key):
        aimessage.append({"role": "user", "content": message})
        #调用api返回回答
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=aimessage
        )
        aimessage.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
        return response["choices"][0]["message"]["content"]
    else:
        return "请输入正确的apikey"

#设置角色函数
def set_character(character_number):
        global promot
        aimessage.clear()
        aimessage.append({"role": "user", "content": promot[character_number]})

#保存文件函数
def save_message():
        global key
        global aimessage
        if len(key) == 51:
            return 0
        content=""
        #判断是否是有效对话
        if  len(aimessage) ==len(aimessage[0]):
            return 0
        message = aimessage
        message.pop(0)   #删除第0行对话
        for sentence in message:   #添加角色
            if sentence["role"] == "assistant":
                content+="chat:"+sentence["content"]+"\n\n"
            else:
                content+="I:"+sentence["content"]+"\n\n"
        #获取合适的文件名
        message.append({"role": "system", "content": "给上面的对话取个简短的标题,不要加引号"})  
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
        )
        filename =  response["choices"][0]["message"]["content"]+".txt"
        #保存文件到当前目录
        f = open(filename, 'x',encoding="utf-8")     
        print(content)
        f.write(content)
        f.close


# 调用api的线程
class MyThread(QThread):
    # 定义一个信号，用于发送数据
    my_signal = pyqtSignal(str)

    def __init__(self,content):
        super(MyThread, self).__init__()
        self.content = content
    # 这里写你的功能函数
    def run(self):
        #回答作为信号发送
        self.my_signal.emit(get_answer(self.content))

# 保存对话文件的线程
class saveThread(QThread):
    my_signal = pyqtSignal(str)
    def __init__(self):
        super(saveThread, self).__init__()
    #保存对话文件
    def run(self):
        save_message()


#主窗口类
class MainWindow(QMainWindow, Ui_ChatBot): # 继承自转换后的类
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 创建UI元素

        # 创建线程实例
        # 调用api的线程
        self.thread = MyThread("")
        # 保存文件的线程
        self.savethread = saveThread()
         # 连接信号和槽
        self.thread.my_signal.connect(self.get_message)
         # 获取组件
        self.chButton_1 = self.findChild(QPushButton, "chButton_1")
        self.chButton_2 = self.findChild(QPushButton, "chButton_2")
        self.chButton_3 = self.findChild(QPushButton, "chButton_3")
        self.chButton_4 = self.findChild(QPushButton, "chButton_4")
        self.chButton_5 = self.findChild(QPushButton, "chButton_5")
        self.chButton_6 = self.findChild(QPushButton, "chButton_6")
        self.savebutton = self.findChild(QPushButton, "savebutton")
        self.sendbutton = self.findChild(QPushButton, "sendbutton")
        self.entey_Edit = self.findChild(QTextEdit, "entey_Edit")
        self.plainTextEdit = self.findChild(QPlainTextEdit, "plainTextEdit")
        self.plainTextEdit.setReadOnly(True)
        self.apikey_edit = self.findChild(QLineEdit, "apikey_edit")

        #  # 绑定按钮点击信号和槽函数  不注释掉会导致Qt的自动连接机制触发，函数可能会执行两次降低程序稳定性
        # self.chButton_1.released.connect(self.on_chButton_1_clicked)
        # self.chButton_2.released.connect(self.on_chButton_2_clicked)
        # self.chButton_3.released.connect(self.on_chButton_3_clicked)
        # self.chButton_4.released.connect(self.on_chButton_4_clicked)
        # self.chButton_5.released.connect(self.on_chButton_5_clicked)
        # self.chButton_6.released.connect(self.on_chButton_6_clicked)
        # self.savebutton.released.connect(self.on_savebutton_clicked)
        # self.sendbutton.released.connect(self.on_sendbutton_clicked)
        
    def get_message(self,text):
        global character
        if character =="人" :
                ch = "Chat"
        else:
            ch = character
        self.plainTextEdit.appendPlainText(ch+":"+text)

    # 定义槽函数
    @pyqtSlot()
    def on_chButton_1_clicked(self):
        set_character(1)
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_2_clicked(self):
        set_character(2)
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_3_clicked(self):
        set_character(3)
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_4_clicked(self):
        set_character(4)
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_5_clicked(self):
        set_character(5)
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_6_clicked(self):
        set_character(6)
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_savebutton_clicked(self):
        self.savethread.start()
    @pyqtSlot()
    def on_sendbutton_clicked(self):
        global key
        if self.apikey_edit.text() !="":
            key = self.apikey_edit.text()
        text = self.entey_Edit.toPlainText()
        if text != "" :
            self.entey_Edit.clear()
            self.plainTextEdit.appendPlainText("我:"+text)
            self.repaint()
            self.thread.content = text
            self.thread.start()#开始回复线程
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    #设置窗口最小尺寸
    window.setMinimumSize(800, 600)
    sys.exit(app.exec_())