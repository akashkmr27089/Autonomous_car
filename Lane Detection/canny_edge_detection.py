# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 22:46:45 2019

@author: akash
"""

import matplotlib.pyplot as plt
import matplotlib.image as imimg
import cv2

image = imimg.imread('exit-ramp.jpg')
plt.imshow(image)

x_size = image.shape[1]
y_size = image.shape[2]

#Converting to GreyScale
gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
plt.imshow(gray_img, cmap='gray')
plt.show()

#Cleaning Image
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)
plt.imshow(blur_gray, cmap='gray')
# Define parameters for Canny and run it
# NOTE: if you try running this code you might want to change these!

#Setting Threshold in such a way that it will reject any gradient less then low_threshold and takes gradient greater then 
#high_threshold as strong point. Finally it will consider all the gradient between low_threshold and hight_threshold 
#including values above hight theshold in such a way that range should be always connected to the above high threshold

low_threshold = 90
high_threshold = 100
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
plt.imshow(edges, cmap='gray')
plt.show()