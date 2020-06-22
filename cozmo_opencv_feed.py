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

startTime = time.time()
maxTime = 60
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)

#orange point: (2,174,188)

orangeLower = (0,164,148)
orangeUpper = (12,184,228)

minRectSize = 10
counter = 0

rect_x = 0
rect_y = 0
rect_w = 0
rect_h = 0
rect_cx = 0
rect_cy = 0

hold_dx = 0
hold_dy = 0
hold_x = 0
hold_y = 0


objectLocation = {"x":0,"y":0,"dx":0,"dy":0} 
def processImage(image):
    global counter
    global rect_x
    global rect_y
    global rect_h
    global rect_w
    global rect_cx
    global rect_cy

    global hold_dx
    global hold_dy
    global hold_x
    global hold_y
    
    #frame = image
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=1280)    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    fHeight = frame.shape[0]
    fWidth = frame.shape[1]
    cx,cy = fWidth/2,fHeight/2
    
    blurred = cv2.GaussianBlur(frame, (11, 11), cv2.BORDER_DEFAULT)
    blurred = frame

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found

    objectLocation["dx"] = hold_dx
    objectLocation["dy"] = hold_dy
    objectLocation["x"] = hold_x
    objectLocation["y"] = hold_y
    
    if len(cnts) > 0 and counter % 10 == 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea) 
        M = cv2.moments(c)
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']) )

        x,y,w,h = cv2.boundingRect(c)
        rect_x = x
        rect_y = y
        rect_w = w
        rect_h = h
        rect_cx = x+(w/2.0)
        rect_cy = y+(h/2.0)
        if np.sqrt(w**2 + h**2) > minRectSize:
            cv2.rectangle(frame, (x,y) , (x+w,y+h) , (0,0,0) , 3)
            cv2.line(frame, (int(rect_cx), int(rect_cy)), (int(rect_cx), int(rect_cy)), (255, 0, 0), thickness=10)
            #cv2.rectangle(frame, (rect_cx,rect_cy) , (5,5) , (255,0,0) , 1)
        dx,dy = cx - x, y - cy
        print('frame width: {}, frame height: {}'.format(fWidth,fHeight))
        print('rectangle x: {}, rectangle y: {}'.format(x,y))
        print('delta x: {}, delta y: {}'.format(dx,dy))
        print('==========================================')
        objectLocation["dx"] = dx
        objectLocation["dy"] = dy
        objectLocation["x"] = x
        objectLocation["y"] = y
        hold_dx = dx
        hold_dy = dy
        hold_x = x
        hold_y = y

    elif counter % 10 != 0:
        cv2.rectangle(frame, (rect_x,rect_y) , (rect_x+rect_w,rect_y+rect_h) , (0,0,0) , 3)
        cv2.line(frame, (int(rect_cx), int(rect_cy)), (int(rect_cx), int(rect_cy)), (255, 0, 0), thickness=10)
        #cv2.rectangle(frame, (rect_cx,rect_cy) , (5,5) , (255,0,0) , 1)
    
    cv2.imshow('image', frame)
    key = cv2.waitKey(1) & 0xFF


def cozmo_program(robot: cozmo.robot.Robot):
    global counter
    robot.camera.color_image_enabled = True #turn on color
    robot.camera.image_stream_enabled = True #turn on camera feed

    time.sleep(2) #allow time to initialize, VERY IMPORTANT
    counter = 0

    while True: #loop images
        image = robot.world.latest_image.raw_image        
        processImage(image)

        if counter % 1 == 0:
            if objectLocation["dx"] > 10 and objectLocation["dx"] < -10:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                print("CENTER CENTER CENTER CENTER CENTER CENTER")
        counter  += 1
        time.sleep(.05)

    cv2.destroyAllWindows()

cozmo.run_program(cozmo_program)
