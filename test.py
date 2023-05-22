# -*- coding: utf-8 -*-
"""
Created on Wed May 17 17:36:11 2023

@author: loveaoe33
"""
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import os
import cv2

Trainfolder_path="C:/Zfn_Data"
Testfolder_path="C:/test_Data"
image_extension=".jpg"
train_images=[]
train_labels=[0]*100
test_images=[]
test_labels=[]



print('\nTest accuracy:')