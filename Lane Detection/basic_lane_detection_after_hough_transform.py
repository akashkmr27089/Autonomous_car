# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 22:59:54 2019

@author: akash
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:39:43 2019

@author: akash
"""

import matplotlib.pyplot as plt
import matplotlib.image as imimg
import cv2
import numpy as np

image = mpimg.imread("exit-ramp.jpg") #Loading Image
ysize = image.shape[0]  #shape of image
xsize = image.shape[1]  
region_select = np.copy(image)

left_1 = [70, 539]    #for selecting the coordinate of left bottom part
left_2 = [458, 230]
right_1 = [498, 231]
right_2 = [900, 539]

fit_left = np.polyfit((left_1[0], left_2[0]), (left_1[1], left_2[1]), 1)
fit_right = np.polyfit((right_1[0], left_2[0]), (right_1[1], left_2[1]), 1)
fit_bottom = np.polyfit((right_1[0], right_2[0]), (right_1[1], right_2[1]),1)

XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*fit_left[0]+fit_left[1])) & (YY > (XX*fit_right[0]+fit_right[1])) & (YY > (XX*fit_bottom[0]+fit_bottom[1]))
region_thresholds2 = np.copy(~region_thresholds)

            
region_select[region_thresholds2] = [0, 0, 0]
print("\n\nfit_bottom {} \nfit_right {}\n fit_left {}".format(fit_bottom, fit_right, fit_left))      
plt.imshow(image)   
plt.show()
plt.imshow(region_select)
plt.show()  


#Converting to GreyScale
gray_img = cv2.cvtColor(region_select, cv2.COLOR_RGB2GRAY)
plt.imshow(gray_img, cmap='gray')
plt.show()

#Cleaning Image
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray_img,(kernel_size, kernel_size), 0)
# Define parameters for Canny and run it
# NOTE: if you try running this code you might want to change these!

#Setting Threshold in such a way that it will reject any gradient less then low_threshold and takes gradient greater then 
#high_threshold as strong point. Finally it will consider all the gradient between low_threshold and hight_threshold 
#including values above hight theshold in such a way that range should be always connected to the above high threshold

low_threshold = 50
high_threshold = 150
masked_edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
plt.imshow(masked_edges)
plt.show()

# As we will be working with Hough transformation with polar coordinates for finding the lines connecting, we will be giving
#value in terms of polar angles and py

rho = 1
theta = np.pi/180
threshold = 1
min_line_length = 10 # It defines the number of line lenght which is accepted for connectino
min_lin_gap = 9 #the more it is, the more it is prone to connecting gaps between lines
line_image = np.copy(image)*0

"""
First off, rho and theta are the distance and angular resolution of our grid in 
Hough space. Remember that, in Hough space, we have a grid laid out along the (Θ, ρ) axis.
 You need to specify rho in units of pixels and theta in units of radians.
 
The threshold parameter specifies the minimum number of votes (intersections in 
a given grid cell) a candidate line needs to have to make it into the output. 
The empty np.array([]) is just a placeholder, no need to change it. min_line_length
 is the minimum length of a line (in pixels) that you will accept in the output, 
 and max_line_gap is the maximum distance (again, in pixels) between segments 
 that you will allow to be connected into a single line. You can then iterate through
 your output lines and draw them onto the image to see what you got!
 
"""
#Hough line detection working using polar coordinates
lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, min_lin_gap)

#Draw lines in the blank lanes for seeing the detection
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)
        
plt.imshow(line_image)

# Create a "color" binary image to combine with line image
color_edges = np.dstack((masked_edges, masked_edges, masked_edges)) 
# Draw the lines on the edge image
combo = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0) 
plt.imshow(combo)
plt.show()
