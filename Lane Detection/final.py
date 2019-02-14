# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 02:12:42 2019

@author: akash
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 01:03:02 2019

@author: akash
"""

from moviepy.editor import VideoFileClip
from IPython.display import HTML
import matplotlib.pyplot as plt
import matplotlib.image as imimg
import cv2
import numpy as np


def pipeline(image):
    region_select = np.copy(image)
    gray_img = cv2.cvtColor(region_select, cv2.COLOR_RGB2GRAY)
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray_img,(kernel_size, kernel_size), 0)
    low_threshold = 50
    high_threshold = 150
    masked_edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1
    theta = np.pi/180
    threshold = 1
    min_line_length = 10 # It defines the number of line lenght which is accepted for connectino
    min_lin_gap = 15 #the more it is, the more it is prone to connecting gaps between lines
    line_image = np.copy(image)*0

    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, min_lin_gap)

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)

    left_1 = [250, 720]    #for selecting the coordinate of left bottom part
    left_2 = [629, 513]
    right_1 = [650, 514]
    right_2 = [936, 720]
    
    ysize = image.shape[0]  #shape of image
    xsize = image.shape[1]  

    fit_left = np.polyfit((left_1[0], left_2[0]), (left_1[1], left_2[1]), 1)
    fit_right = np.polyfit((right_1[0], left_2[0]), (right_1[1], left_2[1]), 1)
    fit_bottom = np.polyfit((right_1[0], right_2[0]), (right_1[1], right_2[1]),1)

    XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
    region_thresholds = (YY > (XX*fit_left[0]+fit_left[1])) & (YY > (XX*fit_right[0]+fit_right[1])) & (YY > (XX*fit_bottom[0]+fit_bottom[1]))
    region_thresholds2 = np.copy(~region_thresholds)
    line_image[region_thresholds2] = [0, 0, 0]   
    
    combo = cv2.addWeighted(image, 0.8, line_image, 1, 0) 
    return combo

"""
image = imimg.imread("data.jpg") #Loading Image
data = pipeline(image)
plt.imshow(data)
plt.show() 
"""
file_output="output.mp4"
clip1 = VideoFileClip("tt1.mp4")
res_clip = clip1.fl_image(pipeline)
res_clip.write_videofile(file_output, audio=False)
#"""