import cozmo

import cv2 
import time
import threading
from collections import deque
import imutils
import numpy as np
import os
from imutils.video import VideoStream
from importlib import reload

image_hsv = None  
pixel = (20,60,80) 

# mouse callback function
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]

        #you might want to adjust the ranges(+-10, etc):
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(pixel, lower, upper)

        image_mask = cv2.inRange(image_hsv,lower,upper)
        cv2.imshow("mask",image_mask)

def cozmo_program(robot: cozmo.robot.Robot):
    import sys
    global image_hsv, pixel # so we can use it in mouse callback
    robot.camera.color_image_enabled = True #turn on color
    robot.camera.image_stream_enabled = True #turn on camera feed

    time.sleep(2) #allow time to initialize, VERY IMPORTANT
    

    image_src = robot.world.latest_image.raw_image
    frame = cv2.cvtColor(np.array(image_src), cv2.COLOR_RGB2BGR)
    #frame = imutils.resize(frame, width=1280)
    
    cv2.imshow("bgr",frame)

    ## NEW ##
    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv', pick_color)

    # now click into the hsv img , and look at values:
    image_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv",image_hsv)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

cozmo.run_program(cozmo_program)