# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:09:29 2019

@author: akash
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

image = mpimg.imread("test.jpg") #Loading Image
ysize = image.shape[0]  #shape of image
xsize = image.shape[1]

color_select = np.copy(image)   #Always make copy of the array as it will help changes in image will not reflect
                                #changes in color_select

#For Selecting the colors which are having value less then some value to make the color to 0
red_threshold = 200
blue_threshold = 200
green_threshold = 200 #For Selecting the color which are having value less then 200
rgb_threshold = [red_threshold, green_threshold, blue_threshold]

threshold = (image[:,:,0]<rgb_threshold[0])|(image[:,:,1]<rgb_threshold[1])|(image[:,:,2]<rgb_threshold[2])
color_select[threshold] = [0,0,0] #this changes the value of those value which are true in threshold

plt.imshow(color_select)
plt.show()

