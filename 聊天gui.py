# 导入Tkinter库
from tkinter import *
import tkinter as tk
import openai
import win32gui
import win32.lib.win32con as win32con


#api key 默认,发布时记得注释掉
openai.api_key = "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"
have_api_key = True


#顶部按钮颜色
top_button_color="#1e6fff"

#默认角色
character = "人"

#字体大小
font_side=15

#字体样式
font_style='YaHei'

# 定义一个函数send_message，用于发送消息并更新聊天记录
def e_send_message(event):
    send_message()

def send_message():


    # 获取输入框中的消息内容
    message = message_entry.get()
    # 如果消息不为空，则在文本框中显示用户发送的消息，并清空输入框
    if message:
        chat_area.insert(END, '我: ' + message + '\n')
        message_entry.delete(0, END)
         # 更新文本框的内容
        chat_area.update_idletasks()
        # 调用聊天机器人的回答函数，并在文本框中显示回答内容,并给它添加answer_tag标签
        answer = get_answer(message)
        chat_area.insert(END,'chat:' + answer + '\n', "answer_tag")


# 定义一个函数get_answer，用于根据用户输入的消息返回聊天机器人
def get_answer(message):
            aimessage.append({"role": "user", "content": message})
            response = chatai()
            aimessage.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
            return response["choices"][0]["message"]["content"]

#调用api
def chatai():
    global have_api_key
    if (api_key_entry.get() != "输入apikey" and api_key_entry.get() != "") or have_api_key:
        if api_key_entry.get() != "输入apikey" and api_key_entry.get():
            openai.api_key = api_key_entry.get()
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=aimessage
        )
        return response
    else:
        return "请输入apikey"

#设置角色函数
def set_character(fun_character):
        global character
        character=fun_character
        aimessage.clear()
        aimessage.append({"role": "user", "content": "现在你要模仿"+character+"和我对话,就像一个真正的"+character+"一样,并且不能暴露你是一个AI或者程序,你要极力隐藏你是个AI或者说程序,下面我们开始正式对话"})
        chat_area.delete('1.0',tk.END)


#保存文件函数
def save_message():
        global aimessage
        global character
        message = aimessage
        content="与"+character+"对话\n\n\n"
        message.pop(0)
        for sentence in message:
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
        f = open(filename, 'x',encoding="utf-8")
        print(content)
        f.write(content)
        f.close

      



 # 获取并隐藏当前的前台窗口
the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)


#创建消息数组
aimessage=[]
aimessage.append({"role": "user", "content": "现在你要模仿"+character+"和我对话,就像一个真正的"+character+"一样,并且不能暴露你是一个AI或者程序,你要极力隐藏你是个AI或者说程序,下面我们开始正式对话"})



# 创建一个名为window的窗口对象
window = Tk()
window.config(bg='#ffffff')
#chatgpt api 调用


# 设置窗口标题为'Chatbot'
window.title('ChatGpt聊天机器人')

# 设置窗口大小为400x500像素
window.geometry('600x700')

#上面的按钮
button_frame = Frame(window) 
button_frame.pack(side=TOP)

# 创建一个名为api_key_entry的输入框对象，用于输入apikey
api_key_entry = Entry(button_frame, bg='#f5f6f7',width=40,font=(font_style, font_side),highlightthickness=0,relief=GROOVE)
api_key_entry.pack(fill=BOTH)
api_key_entry.insert(0,"输入apikey")
# 创建一个名为chat_area的文本框对象，用于显示聊天记录
chat_area = Text(window, bg='#f5f6f7', width=60, height=30,font=(font_style, font_side),highlightthickness=0,relief=GROOVE)
chat_area.pack()



#添加按钮对象
model_1_button = Button(button_frame, text='女朋友', command=lambda: set_character("女朋友"),width=10, height=2,bg=top_button_color,relief=FLAT) 
model_1_button.pack(side=LEFT, padx=2, pady=0)

model_2_button = Button(button_frame, text='男朋友', command=lambda: set_character("男朋友"),width=10, height=2,bg=top_button_color,relief=FLAT) 
model_2_button.pack(side=LEFT, padx=2, pady=0)

model_3_button = Button(button_frame, text='专业的助理', command=lambda: set_character("专业的助理"),width=10, height=2,bg=top_button_color,relief=FLAT) 
model_3_button.pack(side=LEFT, padx=2, pady=0)

model_3_button = Button(button_frame, text='程序员', command=lambda: set_character("程序员"),width=10, height=2,bg=top_button_color,relief=FLAT) 
model_3_button.pack(side=LEFT, padx=2, pady=0)

model_3_button = Button(button_frame, text='猫娘', command=lambda: set_character("一个每句话后面都要加个喵的猫娘"),width=10, height=2,bg=top_button_color,relief=FLAT) 
model_3_button.pack(side=LEFT, padx=2, pady=0)
#保存对话按钮
save_file_button = Button(button_frame, text='保存对话', command=lambda: save_message(),width=10, height=2,bg=top_button_color) 
save_file_button.pack(side=LEFT, padx=2, pady=0)

# 定义一个名为answer_tag的标签，并设置它的前景色为蓝色
chat_area.tag_config("answer_tag", foreground="#4a9bff")

# 创建一个名为message_entry的输入框对象，用于输入消息
message_entry = Entry(window, bg='#f5f6f7',width=40,font=(font_style, font_side),highlightthickness=0,relief=GROOVE)
message_entry.pack(side=LEFT,fill=BOTH)


# 绑定回车键和send_message函数
message_entry.bind("<Return>", e_send_message)

# 创建一个名为send_button的按钮对象，用于触发发送消息函数
send_button = Button(window, text='发送', command=send_message,width=10, height=2,bg='#1e6fff',relief=FLAT)
send_button.pack(side=tk.RIGHT)


# 启动窗口主循环
window.mainloop()