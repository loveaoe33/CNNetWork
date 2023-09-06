# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:16:37 2023

@author: loveaoe33
"""

import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
import SocketConnection
import time
import asyncio
import socket as sock
import traceback
from random import SystemRandom




load_model = tf.keras.models.load_model('Zfn_Train.h5')
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
faces_without_eyes=[]
x=400
y=500
width=200
height=200
Tag="fales"

ResponseText=""
socket_Address=""
socket_Port=""
switch_Function=""



def ImagCheck(face_image):
    face_image=cv2.resize(face_image,(32,32))
    face_image=np.expand_dims(face_image,axis=0)
    Array_images=np.array(face_image)
    predictions=load_model.predict(face_image);
    predicted_class = np.argmax(predictions)  # 取得預測結果的類別索引
    class_names =["立帆","其他"]
    predicted_class_label=class_names[predicted_class]
    '''text_Response.insert(tk.END,predicted_class_label+"\n")'''
    return predicted_class_label


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
    window.after(500, capture_videoMain())
    start_Button.config(state=tk.NORMAL)

def check_Select():
    if(face_Cnn.get()==1 and car_Cnn.get()==1):
        face_Cnn.set(0)
    elif (face_Cnn.get()==1):
        car_Cnn.set(0)
    elif(car_Cnn.get()==1):
        face_Cnn.set(0)
def start_Cv():
    global Tag
    Tag="false"
    capture_video()
    """asyncio.create_task(capture_video())"""
    
def end_Cv():
    global Tag
    Tag="done"
    cap.release()
    canvas.delete("ALL")
    
def capture_video():
    global Tag
    global x
    global y
    global width
    global height
    global faces_without_eyes
    global Tag
    Tag="false"
    cap = cv2.VideoCapture(0)
    
    while Tag != "done":
        ret, frame = cap.read()

        if not ret:
            messagebox.showinfo('提示', 'ret無作動')
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 偵測人臉
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20), maxSize=(300,300))
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))

        if len(faces) > 0:
            text_Response.insert(tk.END,"偵測到人臉\n")
            '''print("偵測到人臉")'''
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

            for (x, y, w, h) in faces:
                Face_has_eyes = False

                for (ex, ey, ew, eh) in eyes:
                    if ex > x and ey > y and ex + ew < x + w and ey + eh < y + h:
                        Face_has_eyes = True
                        break

                if not Face_has_eyes:
                    '''cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) 人臉附近畫框'''
                    faces_without_eyes.append((x, y, w, h))
                    '''return結果'''
                    Result = SocketConnection.main(ImagCheck(frame))
                    '''await asyncio.sleep(0.01)  # 异步等待'''
                    Tag = "done"
                if Tag == "done":
                    if Result:
                      split_Result = Result.split(",")
                      text_Response.insert(tk.END,"偵測人員:"+ split_Result[1] + "\n")
                      messagebox.showinfo('提示', '打卡完成' + split_Result[1])    
                    else:
                      messagebox.showinfo('提示', '後端主機異常')
                break  

        else:
            text_Response.insert(tk.END,"沒偵測到人臉\n")
            '''print("沒偵測到人臉")'''
            cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 2)
        

        # 将图像转换为PIL Image对象
        pil_image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

        # 创建Tkinter图像对象
        tk_image = ImageTk.PhotoImage(image=pil_image)

        # 在画布上显示图像
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        window.update()
        text_Response.see(tk.END)

        # 按下 'q' 键结束程序
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像机资源
    cap.release()
    cv2.destroyAllWindows()



async def asyncWhile():
      capture_video()
      
def capture_videoMain():
    loop = asyncio.get_event_loop()
    loop.create_task(asyncWhile())


    
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
'''tunnel_Select.config(state=tk.DISABLED)'''
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
"""視窗滾軸"""
scrollbar=tk.Scrollbar(window)
scrollbar.place(x=980,y=230,height=350)
scrollbar.config(command=text_Response.yview)
text_Response.config(yscrollcommand=scrollbar.set)
start_Button=tk.Button(window,text="開始識別",command=start_Cv)
start_Button.place(x=300,y=550)
'''start_Button.config(state=tk.DISABLED)'''
end_Button=tk.Button(window,text="停止捕抓",command=end_Cv)
end_Button.place(x=380,y=550)




window.mainloop()