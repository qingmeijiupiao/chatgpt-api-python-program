from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui import Ui_ChatBot # 从ui文件中导入类
import openai
#默认角色
character = "人"

#创建消息数组
aimessage=[]
aimessage.append({"role": "user", "content": "现在你要模仿"+character+"和我对话,就像一个真正的"+character+"一样,并且不能暴露你是一个AI或者程序,你要极力隐藏你是个AI或者说程序,下面我们开始正式对话"})

#api key 默认,发布时记得注释掉
key = "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"

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
def set_character(fun_character):
        global character
        character=fun_character
        aimessage.clear()
        aimessage.append({"role": "user", "content": "现在你要模仿"+character+"和我对话,就像一个真正的"+character+"一样,并且不能暴露你是一个AI或者程序,你要极力隐藏你是个AI或者说程序,下面我们开始正式对话"})

#保存文件函数
def save_message():
        global aimessage
        global character
        if  aimessage == [{"role": "user", "content": "现在你要模仿"+character+"和我对话,就像一个真正的"+character+"一样,并且不能暴露你是一个AI或者程序,你要极力隐藏你是个AI或者说程序,下面我们开始正式对话"}] :
            return 0
        message = aimessage
        content="与"+character+"对话\n\n\n"
        message.pop(0)   #删除第0行对话
        for sentence in message:   #添加角色
            if sentence["role"] == "assistant":
                content+="chat:"+sentence["content"]+"\n\n"
            else:
                content+="I:"+sentence["content"]+"\n\n"
        message.append({"role": "system", "content": "给上面的对话取个简短的标题,不要加引号"})   #获取合适的文件名
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message
        )
        filename =  response["choices"][0]["message"]["content"]+".txt"
        f = open(filename, 'x',encoding="utf-8")     #保存文件到当前目录
        print(content)
        f.write(content)
        f.close


class MainWindow(QMainWindow, Ui_ChatBot): # 继承自转换后的类
    def __init__(self):
        super().__init__()
        self.setupUi(self) # 创建UI元素
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
        self.apikey_edit = self.findChild(QLineEdit, "apikey_edit")


         # 绑定按钮点击信号和槽函数
        self.chButton_1.clicked.connect(self.on_chButton_1_clicked)
        self.chButton_2.clicked.connect(self.on_chButton_2_clicked)
        self.chButton_3.clicked.connect(self.on_chButton_3_clicked)
        self.chButton_4.clicked.connect(self.on_chButton_4_clicked)
        self.chButton_5.clicked.connect(self.on_chButton_5_clicked)
        self.chButton_6.clicked.connect(self.on_chButton_6_clicked)
        self.savebutton.clicked.connect(self.on_savebutton_clicked)
        self.sendbutton.clicked.connect(self.on_sendbutton_clicked)
        
    # 定义槽函数
    @pyqtSlot()
    def on_chButton_1_clicked(self):
        set_character("女朋友")
        self.plainTextEdit.clear()
    
    @pyqtSlot()
    def on_chButton_2_clicked(self):
        set_character("男朋友")
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_3_clicked(self):
        set_character("程序员")
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_4_clicked(self):
        set_character("专业助理")
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_5_clicked(self):
        set_character("猫娘")
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_chButton_6_clicked(self):
        set_character("老师")
        self.plainTextEdit.clear()
    @pyqtSlot()
    def on_savebutton_clicked(self):
        save_message()
    
    @pyqtSlot()
    def on_sendbutton_clicked(self):
        if character =="人" :
            ch = "Chat"
        else:
            ch=character
        text = self.entey_Edit.toPlainText()
        if text != "" :
            self.entey_Edit.clear()
            self.plainTextEdit.appendPlainText("我:"+text)
            self.repaint()
            answer = get_answer(text)
            self.plainTextEdit.appendPlainText(ch+":"+answer)







if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())