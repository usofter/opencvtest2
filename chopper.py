import cv2
import numpy as np
import os
import time

# vid = cv2.VideoCapture('D:\\datasets\\UGOK\\vid_ugok\\VID_20211130_110306.mp4')

# # set video file path of input video with name and extension
vid = cv2.VideoCapture('C:\\Users\\DS\\PycharmProjects\\video_1.avi')

# C:\windows_v1.8.1\ugok_v0.1\calibr
if not os.path.exists('C:\\Users\\DS\\PycharmProjects\\chopped'):
    os.makedirs('C:\\Users\\DS\\PycharmProjects\\chopped')

count=0

#for frame identity
index = 0
while(True):
    vid.set(cv2.CAP_PROP_POS_MSEC, (index * 500)) # every 0.5 second
    # Extract images
    ret, frame = vid.read()
    # end of frames
    if not ret:
        break
    # Saves images
    # name = './images/frame' + str(index) + '.jpg'
    name = 'C:\\Users\\DS\\PycharmProjects\\chopped\\img_' + str(count) + '.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name, frame)


    count+=1
    # next frame
    index += 1
