# -*- coding: utf-8 -*-
import cv2
import time
import tkinter as tk
from tkinter import messagebox
import tensorflow as tf
import numpy as np
import SocketConnection
from SocketConnection import shared_variable
import time

"""
Created on Wed May 17 10:57:14 2023

@author: loveaoe33
"""
load_model = tf.keras.models.load_model('Zfn_Train.h5')
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


eye_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap=cv2.VideoCapture(0)
faces_without_eyes=[]
x=400
y=500
width=200
height=200
count=0
Tag="fales"

def ImagCheck(face_image):
    face_image=cv2.resize(face_image,(32,32))
    face_image=np.expand_dims(face_image,axis=0)
    Array_images=np.array(face_image)
    predictions=load_model.predict(face_image);
    predicted_class = np.argmax(predictions)  # 取得預測結果的類別索引
    class_names =["立帆","其他"]
    predicted_class_label=class_names[predicted_class]
    return predicted_class_label

def CatchImg(count):
    count=count+1
    fileName=f"C:/ZfnData/image_{count}.jpg"
    cv2.imwrite(fileName,frame);
    if count==100:
        messagebox.showinfo('提示', '以存滿一百張')
    
while (Tag!="done"):
    ret, frame=cap.read()
    
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 偵測人臉
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20),maxSize=(300,300))
    eyes=eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))

   
    if len(faces)>0:
        print("偵測到人臉")
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
        
        for(x, y, w, h) in faces:
            Face_has_eyes=False
            
            for(ex, ey, ew, eh) in eyes:
                if ex > x and ey > y and ex + ew < x + w and ey + eh < y + h:
                    Face_has_eyes=True
                    break
               
            if not Face_has_eyes:
                '''cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) 人臉附近畫框'''
                faces_without_eyes.append((x,y,w,h))
                print(ImagCheck(frame))
                '''return結果'''
                if(shared_variable=="FALSE"):
                  Result = SocketConnection.main(ImagCheck(frame))
                  time.sleep(2)
                  Tag="done"
              
                print(Result)

                messagebox.showinfo('提示',Result)
                messagebox.showinfo('提示','偵測到人臉'+ImagCheck(frame))
                break  



    else:
        print("沒偵測到人臉")
        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 2)


    # 顯示影格
    cv2.imshow('Face Detection', frame)

    # 按下 'q' 鍵結束程式
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)

# 釋放攝影機資源
cap.release()
cv2.destroyAllWindows()
    