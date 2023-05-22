# -*- coding: utf-8 -*-
"""
Created on Wed May 17 17:36:11 2023

@author: loveaoe33
"""
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import os
import dlib
import cv2

Trainfolder_path="C:/Zfn_Data"
Testfolder_path="C:/test_Data"
image_extension=".jpg"
train_images=[]
train_labels=[]
test_images=[]
test_labels=[]


def load_images_from_Testfolder(Testfolder_path,current_folder=""):
    global test_images
    global test_labels
    for testfilename in os.listdir(Testfolder_path):
     file_path=os.path.join(Testfolder_path,testfilename)
     print(file_path)
     if os.path.isdir(file_path):
        print(file_path)
        """test_images.extend(load_images_from_Testfolder(file_path,current_folder=os.path.join(current_folder, testfilename)))"""
        load_images_from_Testfolder(file_path,current_folder=os.path.join(current_folder, testfilename))

        print(os.path.isdir(file_path))
        print(current_folder)
     elif testfilename.endswith(image_extension):    
         if current_folder=="class1":
            image = cv2.imread(file_path)
            image = cv2.resize(image, (32, 32))
            image = image / 255.0
            test_images.append(image)
            test_labels.append(0)
            print(len(test_images))


         elif current_folder=="class2":
            image = cv2.imread(file_path)
            image = cv2.resize(image, (32, 32))
            image = image / 255.0
            test_images.append(image)
            test_labels.append(1)
            print(len(test_images))


    return "null"
        

def load_images_from_TrainFolder(Trainfolder_path):
    global train_images
    global train_labels
    for Trainfilename in os.listdir(Trainfolder_path):
     if Trainfilename.endswith(image_extension):
        image_path=os.path.join(Trainfolder_path,Trainfilename)
        image=cv2.imread(image_path)
        image=cv2.resize(image,(32,32))
        image=image/255.0
        train_images.append(image)
        train_labels.append(0)
        """print('load_images_from_TrainFolder555')
        print("train_labels:"+ str(train_labels))
        print("train_images數量:"+ str(len(train_images)))"""

    return "null"

    

load_images_from_TrainFolder(Trainfolder_path)
load_images_from_Testfolder(Testfolder_path,current_folder="")    


print(len(train_images))
print(len(train_labels))
print(len(test_images))
print(len(test_labels)) 
  
train_images=np.array(train_images)  
test_images=np.array(test_images)
train_labels=np.array(train_labels)  
test_labels=np.array(test_labels)  


"""print(len(train_images))
print(len(train_labels))
print(len(test_images))
print(len(test_labels))"""



    
model=tf.keras.Sequential()
model.add (layers.Conv2D(32,(2,2),activation='softmax',input_shape=(32,32,3)))  
"""32,3,3為32個濾波器與3x3大小的捲基層提取特徵  64,64,3為64*64並為3顏色層"""
model.add (layers.MaxPooling2D((2,2)))
model.add (layers.Conv2D(64,(2,2),activation='relu'))
model.add(layers.Dropout(0.5))
model.add (layers.MaxPooling2D((2,2)))
model.add (layers.Conv2D(64,(2,2),activation='relu'))
model.add(layers.Dropout(0.5))
model.add (layers.MaxPooling2D((2,2)))




model.add (layers.Flatten()) 
"""是用於將卷積層的輸出展平（flatten）成一維向量的層。在卷積神經網絡（CNN）中，卷積層通常產生的是多維的特徵圖（feature map），每個特徵圖代表了不同的特徵。然而，在連接全連接層之前，我們需要將這些特徵圖展平成一維向量，以便進行後續的全連接層操作。"""
model.add (layers.Dense(64,activation='softmax')) 
"""是用於定義具有 64 個神經元和 ReLU 激活函數的全連接層"""
model.add (layers.Dense(10, activation='softmax') )  
"""是用於定義具有 64 個神經元和 ReLU 激活函數的全連接層"""

"""編譯細節設定"""
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
print('777')

"""順練前處理"""
"""(train_images,train_labels),(test_images,test_labels)=tf.keras.dataset.cifar10.load_data()
train_images,test_images=train_images/255.0,test_images/255.0"""

model.fit(train_images,train_labels,epochs=50,validation_data=(test_images, test_labels))
test_lost,test_Acc=model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_Acc)
model.save('Zfn_Train.h5')