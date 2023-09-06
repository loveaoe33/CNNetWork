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


model_path="C:\\Users\\loveaoe33\\Desktop\\yolov5\\best.pt"
model=torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
labels = open('C:\\Users\\loveaoe33\\Desktop\\yolov5\\label.txt').read().strip().split('\n')
cudnn.benchmark = True

image_path='C:\\Users\\loveaoe33\\Desktop\\test\\corrtest.jpg'
image=cv2.imread(image_path)
image_No_process=cv2.imread(image_path)
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
Image_width=800
Image_height=400


# image_Iden= model(image)
# for detection in image_Iden.xyxy[0]:
#     xmin, ymin, xmax, ymax, conf, cls = detection.tolist()
#     label = labels[int(cls)]
#     cv2.rectangle(image,(int(xmin), int(ymin)), (int(xmax), int(ymax)),  (0, 255, 0),1)
#     cv2.putText(image, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 1)
#     cropped_image =image[int(ymin):int(ymax),int(xmin):int(xmax)]
# image = cv2.resize(image, (Image_width, Image_height))




width=200
height=100
image=Image.fromarray(image)
# 增強對比度
enhancer = ImageEnhance.Contrast(image)
contrast_image = enhancer.enhance(2)  # 2 表示原始對比度的兩倍

# 增強顏色飽和度
enhancer = ImageEnhance.Color(contrast_image)
colorful_image = enhancer.enhance(2)  # 1.2 表示原始飽和度的1.2倍
# 去除噪點
image = colorful_image.filter(ImageFilter.MedianFilter(size=3))

#二職化
# threshold=40
# image=image.point(lambda p:p > threshold and 255)

image=cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)




# # 使用Canny邊緣檢測
edges = cv2.Canny(image,threshold1=100,threshold2 =200)

# # 執行霍夫變換來檢測直線
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=100, maxLineGap=10)

horizontal_lines=[]
if lines is None:
    print("無直線")
else:
    for line in lines:
        x1,y1,x2,y2=line[0]
        angle=np.arctan2(y2-y1,x2-x1)*180/np.pi
        
        if abs(angle)<10:
            horizontal_lines.append(line[0])

    if len(horizontal_lines) >= 2:
        avg_slope = np.mean([(line[3] - line[1]) / (line[2] - line[0]) for line in horizontal_lines])
        angle_to_rotate = np.arctan(avg_slope) * 180 / np.pi

        center = (image_No_process.shape[1] // 2, image_No_process.shape[0] // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle_to_rotate, scale=1)
        corrected_image = cv2.warpAffine(image_No_process, rotation_matrix, (image_No_process.shape[1], image_No_process.shape[0]), flags=cv2.INTER_LINEAR) ##校正彩色車牌
        corrected_image_gray = cv2.cvtColor(corrected_image,cv2.COLOR_BGR2GRAY) ##車牌轉gray提供角點偵測

        # 使用角点检测器检测角点
        corners = cv2.goodFeaturesToTrack(corrected_image_gray, 100, 0.01,10)
  
        for corner in corners:
             x, y = corner.ravel()
             x, y = int(x), int(y)
             cv2.circle(corrected_image, (x, y), 3, (0, 0, 255), -1) 

        cv2.imshow("Corrected Image", corrected_image)
        cv2.imshow("Corrected Image2", edges)


        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cv2.imshow("Corrected Image", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Not enough horizontal lines detected for calibration.")







# # 定義原始圖像中車牌的四個角點坐標
# original_points = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)

# # 定義目標圖像中車牌的四個角點坐標（例如正確的矩形形狀）
# target_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

# # 計算透視變換矩陣
# perspective_matrix = cv2.getPerspectiveTransform(original_points, target_points)

# # 進行透視變換
# corrected_image = cv2.warpPerspective(image, perspective_matrix, (width, height))






# if lines is not None:
#     for line in lines:
#         rho, theta = line[0]
#         angle_sum += np.degrees(theta)
        
#     average_angle = angle_sum / len(lines)

#     print("平均角度：", average_angle)
#     rows, cols = image.shape[:2]
#     rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), -average_angle, 1)
#     cropped_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
#     # 顯示圖像
#     cv2.imshow('Image', cropped_image)

#     # 等待按下任意按鍵
#     cv2.waitKey(0)

#     # 關閉所有窗口
#     cv2.destroyAllWindows()
# else:
#     print("未偵測到")
#     cv2.imshow('Image', image)
    
#     # 等待按下任意按鍵
#     cv2.waitKey(0)

#     # 關閉所有窗口
#     cv2.destroyAllWindows()