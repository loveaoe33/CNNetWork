# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:31:07 2023

@author: loveaoe33
"""

import cv2
import tensorflow as tf
import os
import dlib
from PIL import Image, ImageTk
import tkinter as tk
from openalpr import Alpr
from tkinter import messagebox
import numpy as np




window=tk.Tk()
window.geometry("1000x600")
Car_Data_path="C:/Car_Data"
current_image_index=0
Images=[]
canvas_width=0
canvas_height=0
Image_width=0
Image_height=0
input_size = (416, 416)
Car_labels =[]
alpr =Alpr("eu", "/openalpr-master/config", "/openalpr-master/runtime_data")

def Load_Alpr():
    if not alpr.is_loaded():
        messagebox.showinfo('提示', 'Alpr位成功載入!')
        sys.exiit(1)

def Load_Images():
    global Car_Data_path
    for filename in os.listdir(Car_Data_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image=Image.open(os.path.join(Car_Data_path,filename))
            Images.append(image)
            

def _init_Ui():
    global Images,canvas,canvas_width,canvas_height,Image_width,Image_height
    canvas_width=400
    canvas_height=300
    canvas=tk.Canvas(window,width=canvas_width,height=canvas_height)
    canvas.pack()


def show_image():
    global Images,current_image_index,photo,Image_width,Image_height
    Image_width=800
    Image_height=400
    canvas.delete("all")
    # 縮放圖片以符合畫布尺寸
    image=Images[current_image_index]
    image.thumbnail((Image_width, Image_height))
     # 將PIL圖片轉換為Tkinter圖片
    photo=ImageTk.PhotoImage(image)
    image_data =np.array(image)
     # 在畫布上顯示圖片
    canvas.create_image(0,0,anchor=tk.NW, image=photo)
    identify_image(process_image(image_data))
    # 設定按鈕初始狀態
    prev_button.config(state=tk.NORMAL if current_image_index>0 else tk.DISABLED)
    next_button.config(state=tk.NORMAL if current_image_index < len(Images) - 1 else tk.DISABLED)


def prev_image():
    global current_image_index
    if current_image_index:
        current_image_index -=1
        show_image()
        
def next_image():
    global current_image_index
    if current_image_index < len(Images) - 1:
        current_image_index += 1
        show_image()
"""車牌欲處理"""
def process_image(Target_image):
    blod=cv2.dnn.blobFromImage(Target_image,1/255.0,input_size,swapRB=True, crop=False)
    
    return blod
    
    
"""車牌處理切割"""  
def shot_image(Target_image): 
     Trans_image=process_image(Target_image)
     gray = cv2.cvtColor(Target_image, cv2.COLOR_BGR2GRAY)
     
     
     # 應用閾值處理以獲取二值化圖像
     _, binary=cv2.threshold (gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
     # 進行輪廓檢測
     contours, _=cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     license_plate_contour=None
     for contour in contours:
         x,y,w,h=cv2.boundingRect(contour)
         aspect_ratio=w / float(h)
         area =cv2.contourArea(contour)
         rectangularity = area / (w * h)


         if area > 1000 and 2 < aspect_ratio < 4 and 0.5 < rectangularity < 1.0:
             license_plate_contour=contour
             break
     if license_plate_contour is not None:
         x, y, w, h = cv2.boundingRect(license_plate_contour)
         cv2.rectangle(Target_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
         
         license_plate=Target_image[y:y + h, x:x + w]
         cv2.imshow("License Plate", license_plate)
         cv2.waitKey(0)
         cv2.destroyAllWindows()
     else:
         print("找不到車牌區域")

     
 
 
'''def shot_image(Target_image): 
    TargetProcess_image=process_image(Target_image)
    net.setInput(TargetProcess_image)
    detections =net.forward()
    for detection in detections:
        confidence =detection[4]
        if confidence >0.5:# 設定置信度閾值
            x,y,w,h=detection[0:4] * np.array([Target_image.shape[1], Target_image.shape[0], Target_image.shape[1], Target_image.shape[0]])
            x, y, w, h = int(x - w/2), int(y - h/2), int(w), int(h)
            cv2.rectangle(Target_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(Target_image, Car_labels[0], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return Target_image'''
    


"""使用apr辨識"""
def identify_image(Target_image):
    if not alpr.is_loaded():
       print("OpenALPR 初始化失敗。請確保已安裝相關配置文件和運行時數據。")
       exit(1)
    else:
        alpr.set_top_n(3)
        alpr.set_default_region("eu")
        results=Apr.recognize_ndarray(ndarray=Target_image)
        for plate in results['results']:
            for candidate in plate['candidates']:
                plate_nuber=candiate['plate']
                confidence=candiate['confidence']
                print("車牌號碼：", plate_number)
                print("信心分數：", confidence)
    Apr.unload()
    
    

prev_button=tk.Button(window, text="上一張", command=prev_image, state=tk.DISABLED) 
prev_button.place(x=430,y=480)

next_button=tk.Button(window, text="下一張", command=next_image, state=tk.NORMAL) 
next_button.place(x=480,y=480)
Load_Images()
_init_Ui()
show_image()
window.mainloop()
