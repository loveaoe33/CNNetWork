# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:16:37 2023

@author: loveaoe33
"""

import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk



socket_Address=""
socket_Port=""
switch_Function=""
cap=""
    

def get_Text():
    global socket_Address
    global socket_Port
    socket_Address=text_Address.get()
    socket_Port=text_Port.get()
    if(socket_Address=="" or socket_Port==""):
        messagebox.showinfo('提示', '不可為空')
    else:
        messagebox.showinfo('提示', socket_Address+socket_Port)
        tunnel_Select.config(state=tk.NORMAL)


    print("地址:"+socket_Address+"Port號:"+socket_Port)

def cnn_Function():
    global switch_Function
    if(face_Cnn.get()==1):
        switch_Function="Face"
        print("選擇臉部辨識")
    elif(car_Cnn.get()==1):
        switch_Function="Car"
        print("選擇車牌辨識")
    else:
        messagebox.showinfo('提示', '至少選擇一項功能')
    window.after(500, capture_video)
    start_Button.config(state=tk.NORMAL)

def check_Select():
    if(face_Cnn.get()==1 and car_Cnn.get()==1):
        face_Cnn.set(0)
    elif (face_Cnn.get()==1):
        car_Cnn.set(0)
    elif(car_Cnn.get()==1):
        face_Cnn.set(0)
def start_Cv():
    capture_video()
    
def capture_video():
    global cap
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 转换图像格式，从BGR转为RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        # 将图像转换为PIL Image对象
        pil_image = Image.fromarray(image)

        # 创建Tkinter图像对象
        tk_image = ImageTk.PhotoImage(image=pil_image)

        # 在画布上显示图像
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        window.update()

    cap.release()

def end_Cv():
    cap.release()
    canvas.delete("ALL")
    
window = tk.Tk()
window.geometry("1000x600")

window.title("人臉辨識/車牌辨識選擇器")
label = tk.Label(window,text="請輸入相關訊並勾選")
label.place(x=770, y=0)

label_Address=tk.Label(window,text="請輸入Address")
label_Address.place(x=770, y=80)

text_Address=tk.Entry(window)
text_Address.place(x=770, y=100)

label_Port=tk.Label(window,text="請輸入Port")
label_Port.place(x=770, y=130)

text_Port=tk.Entry(window)
text_Port.place(x=770, y=150)


socket_Button=tk.Button(window,text="建立通道",command=get_Text)
socket_Button.place(x=770,y=170)

tunnel_Select=tk.Button(window,text="使用功能",command=cnn_Function)
tunnel_Select.place(x=850,y=170)
tunnel_Select.config(state=tk.DISABLED)


face_Cnn=tk.IntVar()
checkbox1=tk.Checkbutton(window, text="臉部辨識", variable=face_Cnn,command=check_Select)
checkbox1.place(x=750,y=200)

car_Cnn=tk.IntVar()
checkbox2=tk.Checkbutton(window, text="車牌辨識", variable=car_Cnn,command=check_Select)
checkbox2.place(x=830,y=200)

canvas=tk.Canvas(window, width=600, height=500)
canvas.place(x=50,y=50)

text_Response=tk.Text(window,height="25",width="45")
text_Response.place(x=670,y=230)

start_Button=tk.Button(window,text="開始識別",command=start_Cv)
start_Button.place(x=300,y=550)
start_Button.config(state=tk.DISABLED)

end_Button=tk.Button(window,text="停止捕抓",command=end_Cv)
end_Button.place(x=380,y=550)




window.mainloop()