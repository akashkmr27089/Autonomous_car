# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:39:43 2019

@author: akash
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

image = mpimg.imread("test.jpg") #Loading Image
ysize = image.shape[0]  #shape of image
xsize = image.shape[1]  
region_select = np.copy(image)

left_bottom = [120, 539]    #for selecting the coordinate of left bottom part
right_bottom = [800, 539]   #for selecting the area in the right bottom part
apex = [470, 310]           #for selecting the coordinate for middle point in triangle

fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*fit_left[0] + fit_left[1])) & (YY > (XX*fit_right[0] + fit_right[1])) & (YY < (XX*fit_bottom[0] + fit_bottom[1]))

region_thresholds2 = np.copy(~region_thresholds)
            
region_select[region_thresholds2] = [0, 0, 0]
print("\n\nfit_bottom {} \nfit_right {}\n fit_left {}".format(fit_bottom, fit_right, fit_left))      
plt.imshow(image)   
plt.show()
plt.imshow(region_select)
plt.show()  

################# FOR FINDING THE LANE OF THE SELECTED LANES #######################
color_select = np.copy(region_select)
#For Selecting the colors which are having value less then some value to make the color to 0
red_threshold = 200
blue_threshold = 200
green_threshold = 200 #For Selecting the color which are having value less then 200
rgb_threshold = [red_threshold, green_threshold, blue_threshold]

data = np.copy(image)
color_thresholds = (region_select[:,:,0]<rgb_threshold[0])|(region_select[:,:,1]<rgb_threshold[1])|(region_select[:,:,2]<rgb_threshold[2])
color_thresholds2 = ~color_thresholds
data[color_thresholds2] = [255,0,0] #this changes the value of those value which are true in threshold

plt.imshow(data)
plt.show()