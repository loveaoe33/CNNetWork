# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:31:07 2023

@author: loveaoe33
"""

import cv2

import os
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import messagebox
import numpy as np
import torch
import torchvision.transforms as transforms
from torch.backends import cudnn
import pytesseract
import easyocr


window=tk.Tk()

os.environ['TESSDATA_PREFIX'] = r'C:\Users\loveaoe33\anaconda3\envs\yolov5\tessdata'
tessdata_dir='C:\\Users\\loveaoe33\\anaconda3\\envs\\yolov5\\tessdata'

model_path="C:\\Users\\loveaoe33\\Desktop\\yolov5\\best.pt"
model=torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
labels = open('C:\\Users\\loveaoe33\\Desktop\\yolov5\\label.txt').read().strip().split('\n')
cudnn.benchmark = True
window.geometry("1000x1000")
Car_Data_path="C:/Users/loveaoe33/Desktop/test"
current_image_index=0
Images=[]
canvas_width=0
canvas_height=0
Image_width=0
Image_height=0
input_size = (416, 416)
Car_labels =[]
cropped_image=None
tk_proess_Image=None
reader = easyocr.Reader(['en'])


def Load_Images():
    global Car_Data_path
    for filename in os.listdir(Car_Data_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path=os.path.join(os.path.join(Car_Data_path,filename))
            image = cv2.imread(image_path)  
            Images.append(image)
            

def _init_Ui():
    global Images,canvas,canvas_width,canvas_height,Image_width,Image_height
    canvas_width=800
    canvas_height=500
    canvas=tk.Canvas(window,width=canvas_width,height=canvas_height)
    canvas.pack()


def show_image():
    global Images,current_image_index,photo,Image_width,Image_height,cropped_image 
    Image_width=800
    Image_height=400
    canvas.delete("all")
    # 縮放圖片以符合畫布尺寸
    image=cv2.cvtColor(Images[current_image_index], cv2.COLOR_BGR2GRAY) 

    '''image_Size=cv2.resize(image, (1024, 1024))'''
    image_Iden= model(image)
    label_frame = tk.Frame(canvas, bg='white')
    canvas.create_window(0, 0, anchor=tk.NW, window=label_frame, width=Image_width, height=Image_height)
    for detection in image_Iden.xyxy[0]:
        xmin, ymin, xmax, ymax, conf, cls = detection.tolist()
        label = labels[int(cls)]
        cv2.rectangle(image,(int(xmin), int(ymin)), (int(xmax), int(ymax)),  (0, 255, 0),1)
        cv2.putText(image, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 1)
        cropped_image =image[int(ymin):int(ymax),int(xmin):int(xmax)]
        
    image = cv2.resize(image, (Image_width, Image_height))
    image_pil=Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
     # 將PIL圖片轉換為Tkinter圖片
    photo=ImageTk.PhotoImage(image_pil)
     # 在畫布上顯示圖片
    canvas.create_image(0,0,anchor=tk.NW, image=photo)
    # 設定按鈕初始狀態
    prev_button.config(state=tk.NORMAL if current_image_index>0 else tk.DISABLED)
    next_button.config(state=tk.NORMAL if current_image_index < len(Images) - 1 else tk.DISABLED)
    image_label = tk.Label(label_frame, image=photo)
    image_label.pack()
    show_process_Image(cropped_image)
    canvas.update()



def text_iden(text_image):
    # pil_image=Image.fromarray(text_image)
    # process_text=pytesseract.image_to_string(text_image, lang='eng', config='--tessdata-dir {}'.format(tessdata_dir))
    results_tran=np.array(text_image)
    # cv2Result=cv2.cvtColor(np.array(text_image),cv2.COLOR_RGB2BGR)
    # img = cv2.imread('C:\\Users\\loveaoe33\\Desktop\\test\\test.jpg')
    # print(img)

    results = reader.readtext(results_tran)
    print(results)




  #車牌顯現區域
def show_process_Image(cropped_image):
    global tk_proess_Image
    # if cropped_image is not None:
    #     cv2.imshow('Process_Image', cropped_image )
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()


    # 將圖像轉換為 PIL Image 物件
    pil_Image=Image.fromarray(cropped_image)
    Buffer_Image=pil_process_image(pil_Image)
    # 將 PIL Image 轉換為 Tkinter 的 Image 物件
    tk_proess_Image=ImageTk.PhotoImage(Buffer_Image)
    label_image =tk.Label(window,image=tk_proess_Image)
    label_image.place(x=500,y=510)



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
    gray_image=cv2.cvtColor(Target_image, cv2.COLOR_BGR2GRAY)
    # 進行二值化處理
    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    denoised_image=cv2.medianBlur(threshold_image, 3)
    return denoised_image
"""PIL車牌欲處理""" 
def pil_process_image(Target_image):
    x1, y1 = 100, 200  # 假設車牌的左上角座標是 (100, 200)
    x2, y2 = 300, 200  # 假設車牌的右上角座標是 (300, 200)
    x3, y3 = 300, 300  # 假設車牌的右下角座標是 (300, 300)
    x4, y4 = 100, 300  # 假設車牌的左下角座標是 (100, 300)
    # #PILToOpenCv
    # CV_Image=np.array(Target_image)
    plate_corners_Image=np.array(Target_image)
    plate_corners = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype='float32')

    # 定義車牌校正後的矩形區域
    plate_width, plate_height = (200, 100)  # 假設車牌的寬度和高度
    corrected_corners = np.array([[0, 0], [plate_width, 0], [plate_width, plate_height], [0, plate_height]], dtype='float32')

    # 進行透視變換，將車牌校正為矩形
    perspective_matrix = cv2.getPerspectiveTransform(plate_corners, corrected_corners)
    corrected_plate = cv2.warpPerspective(plate_corners_Image, perspective_matrix, (plate_width, plate_height))
    
    # equalized_image = cv2.equalizeHist(CV_Image)
    # # CVToPIL
    # equalized_image=Image.fromarray(equalized_image)
    corrected_plate=Image.fromarray(corrected_plate)
    # 增強對比度
    enhancer = ImageEnhance.Contrast(corrected_plate)
    contrast_image = enhancer.enhance(2)  # 2 表示原始對比度的兩倍

    # 增強顏色飽和度
    enhancer = ImageEnhance.Color(contrast_image)
    colorful_image = enhancer.enhance(1.2)  # 1.2 表示原始飽和度的1.2倍

    # # 增強對比度
    # enhancer = ImageEnhance.Contrast(colorful_image)
    # image = enhancer.enhance(2)  # 2 表示原始對比度的兩倍
    # 去除噪點
    image = colorful_image.filter(ImageFilter.MedianFilter(size=3))

    #灰階
    # gray_image = image.convert("L")
   
    #二值化
    threshold=40
    binary_image=image.point(lambda p:p > threshold and 255)

    text_iden(binary_image)

    return binary_image


"""車牌處理切割"""  
# def shot_image(Target_image): 
#      Trans_image=process_image(Target_image)
#      gray = cv2.cvtColor(Target_image, cv2.COLOR_BGR2GRAY)
     
     
#      # 應用閾值處理以獲取二值化圖像
#      _, binary=cv2.threshold (gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#      # 進行輪廓檢測
#      contours, _=cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#      license_plate_contour=None
#      for contour in contours:
#          x,y,w,h=cv2.boundingRect(contour)
#          aspect_ratio=w / float(h)
#          area =cv2.contourArea(contour)
#          rectangularity = area / (w * h)


#          if area > 1000 and 2 < aspect_ratio < 4 and 0.5 < rectangularity < 1.0:
#              license_plate_contour=contour
#              break
#      if license_plate_contour is not None:
#          x, y, w, h = cv2.boundingRect(license_plate_contour)
#          cv2.rectangle(Target_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
         
#          license_plate=Target_image[y:y + h, x:x + w]
#          cv2.imshow("License Plate", license_plate)
#          cv2.waitKey(0)
#          cv2.destroyAllWindows()
#      else:
#          print("找不到車牌區域")

     
 
 
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
    print("123")

    
    

prev_button=tk.Button(window, text="上一張", command=prev_image, state=tk.DISABLED) 
prev_button.place(x=530,y=680)

next_button=tk.Button(window, text="下一張", command=next_image, state=tk.NORMAL) 
next_button.place(x=580,y=680)




Load_Images()
_init_Ui()
show_image()
window.mainloop()
