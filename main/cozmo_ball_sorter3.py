##Still a work in progress for the turning parts of the program

import cozmo
from cozmo.util import *
import cv2 
import time
import threading
from collections import deque
import imutils
import numpy as np
import os
from imutils.video import VideoStream
from importlib import reload
import PIL
from PIL import ImageFilter

startTime = time.time()
maxTime = 60

#orange point: (2,174,188)
###################ORANGE GLOBAL VARIABLES#########################
#orangeLower = (0,164,148)
#orangeUpper = (12,184,228)
orangeLower = (0,135,140)
orangeUpper = (24,210,255)

orangeMinRectSize = 3000
orangeCounter = 0

orangeRect_x = 0
orangeRect_y = 0
orangeRect_h = 0
orangeRect_w = 0
orangeRect_cx = 0
orangeRect_cy = 0

orangeHold_dx = 0
orangeHold_dy = 0
orangeHold_x = 0
orangeHold_y = 0

############GREEN GLOBAL VARIABLES#########################
greenLower = (47, 54, 10)
greenUpper = (80, 155, 150)

greenMinRectSize = 3000
greenCounter = 0

greenRect_x = 0
greenRect_y = 0
greenRect_h = 0
greenRect_w = 0
greenRect_cx = 0
greenRect_cy = 0

greenHold_dx = 0
greenHold_dy = 0
greenHold_x = 0
greenHold_y = 0

greenCentered = False


def detectGreenBall(image):
    global greenCounter
    global greenRect_x
    global greenRect_y
    global greenRect_h
    global greenRect_w
    global greenRect_cx
    global greenRect_cy

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
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # only proceed if at least one contour was found

    drawGreenRect = False #boolean value to see in the rectangle is large enough
    
    if len(cnts) > 0 and greenCounter % 1 == 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea) 
        M = cv2.moments(c)
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']) )

        x,y,w,h = cv2.boundingRect(c)
        greenRect_x = x
        greenRect_y = y
        greenRect_w = w
        greenRect_h = h
        rect_area = w * h
        greenRect_cx = x+(w/2.0)
        greenRect_cy = y+(h/2.0)
        if rect_area > greenMinRectSize:
            drawGreenRect = True
            cv2.rectangle(frame, (greenRect_x, greenRect_y) , (greenRect_x + greenRect_w, greenRect_y + greenRect_h) , (0,0,0) , 3)
            #cv2.putText(frame,(str(rect_cx) + ' ' + str(rect_cy) + '\nwidth: ' + str(rect_w)), (int(rect_cx), int(rect_cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            cv2.line(frame, (int(greenRect_cx), int(greenRect_cy)), (int(greenRect_cx), int(greenRect_cy)), (255, 0, 0), thickness=10)
            #cv2.rectangle(frame, (rect_cx,rect_cy) , (5,5) , (255,0,0) , 1)
        dx,dy = cx - x, y - cy

    elif len(cnts) == 0 or rect_area < greenMinRectSize: #if there is no contour or if the contour is too small set the variables to None
        greenRect_cx = None
        greenRect_w = None
        greenRect_h = None
        print("None")
             

    #elif counter % 5 != 0:
    #    cv2.rectangle(frame, (rect_x,rect_y) , (rect_x+rect_w,rect_y+rect_h) , (0,0,0) , 3)
    #    cv2.putText(frame,(str(rect_cx) + ' ' + str(rect_cy)), (int(rect_cx), int(rect_cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    #    cv2.line(frame, (int(rect_cx), int(rect_cy)), (int(rect_cx), int(rect_cy)), (255, 0, 0), thickness=10)
        #cv2.rectangle(frame, (rect_cx,rect_cy) , (5,5) , (255,0,0) , 1)
    
    return drawGreenRect,greenRect_x,greenRect_y,greenRect_w,greenRect_h,greenRect_cx,greenRect_cy #return these values to draw with drawing function
    
    #cv2.imshow('image', greenFrame)
    #key = cv2.waitKey(1) & 0xFF

def detectOrangeTray(image):
    global orangeCounter
    global orangeRect_x
    global orangeRect_y
    global orangeRect_h
    global orangeRect_w
    global orangeRect_cx
    global orangeRect_cy

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

    # construct a mask for the color "orange", then perform
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

    drawOrangeRect = False #boolean value to see in the rectangle is large enough
    
    if len(cnts) > 0 and orangeCounter % 1 == 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea) 
        M = cv2.moments(c)
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']) )

        x,y,w,h = cv2.boundingRect(c)
        orangeRect_x = x
        orangeRect_y = y
        orangeRect_w = w
        orangeRect_h = h
        rect_area = w * h
        orangeRect_cx = x+(w/2.0)
        orangeRect_cy = y+(h/2.0)
        if rect_area > orangeMinRectSize:
            drawOrangeRect = True
            cv2.rectangle(frame, (orangeRect_x, orangeRect_y) , (orangeRect_x + orangeRect_w, orangeRect_y + orangeRect_h) , (0,0,0) , 3)
            #cv2.putText(frame,(str(rect_cx) + ' ' + str(rect_cy) + '\nwidth: ' + str(rect_w)), (int(rect_cx), int(rect_cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            cv2.line(frame, (int(orangeRect_cx), int(orangeRect_cy)), (int(orangeRect_cx), int(orangeRect_cy)), (255, 0, 0), thickness=10)
            #cv2.rectangle(frame, (rect_cx,rect_cy) , (5,5) , (255,0,0) , 1)
        dx,dy = cx - x, y - cy

    elif len(cnts) == 0 or rect_area < orangeMinRectSize: #if there is no contour or if the contour is too small set the variables to None
        orangeRect_cx = None
        orangeRect_w = None
        orangeRect_h = None
        print("None")
             

    #elif counter % 5 != 0:
    #    cv2.rectangle(frame, (rect_x,rect_y) , (rect_x+rect_w,rect_y+rect_h) , (0,0,0) , 3)
    #    cv2.putText(frame,(str(rect_cx) + ' ' + str(rect_cy)), (int(rect_cx), int(rect_cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    #    cv2.line(frame, (int(rect_cx), int(rect_cy)), (int(rect_cx), int(rect_cy)), (255, 0, 0), thickness=10)
        #cv2.rectangle(frame, (rect_cx,rect_cy) , (5,5) , (255,0,0) , 1)
    
    return drawOrangeRect,orangeRect_x,orangeRect_y,orangeRect_w,orangeRect_h,orangeRect_cx,orangeRect_cy #return these values to draw with drawing function
    
    #cv2.imshow('image', orangeFrame)
    #key = cv2.waitKey(1) & 0xFF

def drawRectangles(image, greenDrawBool, g_x, g_y, g_w, g_h, g_cx, g_cy, orangeDrawBool, o_x, o_y, o_w, o_h, o_cx, o_cy):
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=1280)   
    
    if greenDrawBool: #draws if the green rectangle is large enough
        cv2.rectangle(frame, (g_x, g_y) , (g_x + g_w, g_y + g_h) , (0,255,0) , 3)
        #cv2.putText(frame,(str(rect_cx) + ' ' + str(rect_cy) + '\nwidth: ' + str(rect_w)), (int(rect_cx), int(rect_cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.line(frame, (int(g_cx), int(g_cy)), (int(g_cx), int(g_cy)), (255, 0, 0), thickness=10)
        
    if orangeDrawBool: #draws if the orange rectangle is large enough
        cv2.rectangle(frame, (o_x, o_y) , (o_x + o_w, o_y + o_h) , (0,0,255) , 3)
        #cv2.putText(frame,(str(rect_cx) + ' ' + str(rect_cy) + '\nwidth: ' + str(rect_w)), (int(rect_cx), int(rect_cy)), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.line(frame, (int(o_cx), int(o_cy)), (int(o_cx), int(o_cy)), (255, 0, 0), thickness=10)
        
    cv2.imshow('image', frame)
    key = cv2.waitKey(1) & 0xFF
    
    
###############################END OF COLOR DETECTION FUNCTIONS##########################################################    

pickingBall = 0
findingGoal = 0
droppingBall = 0

def cozmo_get_speed(color):    
    global greenRect_cx
    global greenRect_cy
    global orangeRect_cx
    global orangeRect_cy
    
    speed = 0
    if color == 1: # green
        if greenRect_cx != None:
            centerDifference = 640 - greenRect_cx
        else:
             centerDifference = 300

        speed = centerDifference/10.0
        if speed < 5:
            speed = 5
        elif speed > 15:
            speed = 15
        return speed
    elif color == 2: # orange
        if orangeRect_cx != None:
            centerDifference = 640 - orangeRect_cx
        else:
            centerDifference = 300
        speed = centerDifference/10.0
        if speed < 5:
            speed = 5
        elif speed > 15:
            speed = 15
        return speed
    

def cozmoFindGreenBall(robot: cozmo.robot.Robot,tolerance,greenRect_w_limit):
    global greenCounter
    global greenCentered
    global greenRect_cx
    global greenRect_w
    global pickingBall
    global findingGoal
    global droppingBall

    upperLimit = 640 + tolerance
    lowerLimit = 640 - tolerance
    
    lastTurn = 1 #right turn
    sleepTime = 0.1
    while greenCounter % 1 == 0 and pickingBall == 0 and findingGoal == 0 and droppingBall == 0:
        speed = cozmo_get_speed(1)
        print(greenRect_w)
        if greenRect_cx != None:
            if greenRect_cx > upperLimit:
                robot.drive_wheel_motors(speed,-speed)
                #time.sleep(sleepTime)
                lastTurn = 1
                greenCentered = False
            elif greenRect_cx < lowerLimit:
                robot.drive_wheel_motors(-speed,speed)
                #time.sleep(sleepTime)
                lastTurn = 0
                greenCentered = False
            else:
                #robot.drive_wheel_motors(0,0)
                greenCentered = True

            #print(str(greenCentered) + ' rectangle width: ' + str(greenRect_w) + ' rectangle limit: ' + str(greenRect_w_limit))

            if greenCentered: #when the robot is greenCentered on a ball, start moving towards it
                speed = cozmo_get_speed(1)
                if greenRect_w < greenRect_w_limit:
                    robot.drive_wheel_motors(20,20)
                    #time.sleep(sleepTime)
                elif greenRect_w > greenRect_w_limit + 50:
                    robot.drive_wheel_motors(-20,-20)
                    #time.sleep(sleepTime)    
                else:
                    robot.drive_wheel_motors(0,0)
                    pick_ball(robot)
        
        else:
            if lastTurn == 1 and greenRect_cx == None: #continue turning right to try and find a contour
                robot.drive_wheel_motors(speed,-speed)
                print("turning right to find contour")
                greenCentered = False
                
            elif lastTurn == 0 and greenRect_cx == None: #turn left to try and find contour
                robot.drive_wheel_motors(-speed,speed)
                print("turning left to find contour")
                greenCentered = False

def pick_ball(robot: cozmo.robot.Robot):
    global pickingBall
    speed = 20
    pickingBall = 1
    if pickingBall == 1:
        robot.set_lift_height(height=1.0).wait_for_completed()
        #move_lift(robot,10,2)
        robot.drive_wheel_motors(35,35)
        time.sleep(2)
        robot.drive_wheel_motors(0,0) 
        robot.set_lift_height(height=0.0).wait_for_completed()
        #move_lift(robot,-10,2)
        robot.drive_wheel_motors(35,35)
        time.sleep(2)
        robot.drive_wheel_motors(0,0)
        robot.set_lift_height(height=1.0).wait_for_completed()
        #move_lift(robot,10,2)
        pickingBall = 2
        find_goal(robot,50,1100)
    print("done")

def find_goal(robot: cozmo.robot.Robot,tolerance,orangeRect_w_limit):
    global pickingBall
    global findingGoal
    global droppingBall
    global orangeCounter
    global orangeCentered
    global orangeRect_cx
    global orangeRect_w
    
    upperLimit = 640 + tolerance
    lowerLimit = 640 - tolerance
    
    lastTurn = 1 #right turn
    sleepTime = 0.1
    findingGoal = 1
    
    while pickingBall == 2 and findingGoal == 1 and droppingBall == 0: # if ball has been picked update
    #while orangeCounter % 1 == 0 and pickingBall == 2 and findingGoal == 1:
        speed = cozmo_get_speed(2)
        #print('finding goal')
        print(str(orangeRect_w) + " finding goal")
        if orangeRect_cx != None:
            if orangeRect_cx > upperLimit:
                robot.drive_wheel_motors(speed,-speed)
                #time.sleep(sleepTime)
                lastTurn = 1
                orangeCentered = False
            elif orangeRect_cx < lowerLimit:
                robot.drive_wheel_motors(-speed,speed)
                #time.sleep(sleepTime)
                lastTurn = 0
                orangeCentered = False
            else:
                #robot.drive_wheel_motors(0,0)
                orangeCentered = True

            #print(str(orangeCentered) + ' rectangle width: ' + str(orangeRect_w) + ' rectangle limit: ' + str(greenRect_w_limit))

            if orangeCentered: #when the robot is orangeCentered on a ball, start moving towards it
                speed = cozmo_get_speed(2)
                if orangeRect_w < orangeRect_w_limit:
                    robot.drive_wheel_motors(20,20)
                    #time.sleep(sleepTime)
                elif orangeRect_w > orangeRect_w_limit + 50:
                    robot.drive_wheel_motors(-20,-20)
                    #time.sleep(sleepTime)    
                else:
                    robot.drive_wheel_motors(0,0)
                    findingGoal = 0
                    drop_ball(robot)
        
        else:
            if lastTurn == 1 and orangeRect_cx == None: #continue turning right to try and find a contour
                robot.drive_wheel_motors(speed,-speed)
                print("turning right to find contour")
                orangeCentered = False
                
            elif lastTurn == 0 and orangeRect_cx == None: #turn left to try and find contour
                robot.drive_wheel_motors(-speed,speed)
                print("turning left to find contour")
                orangeCentered = False
    
    #code for finding spot for ball to be dropped     
    
def drop_ball(robot: cozmo.robot.Robot): #function for dropping the ball after it finds the spot
    global droppingBall
    global pickingBall
    global findingGoal
    speed = 20
    droppingBall = 1
    if droppingBall == 1 and findingGoal == 0:
        robot.drive_wheel_motors(35,35) #have to move robot forward more in order to drop the ball in 
        time.sleep(3)
        robot.drive_wheel_motors(0,0)
        robot.set_lift_height(height=0.3).wait_for_completed()
        #move_lift(robot,10,2)
        robot.drive_wheel_motors(-35,-35)
        time.sleep(1.5)
        robot.drive_wheel_motors(0,0) 
        robot.set_lift_height(height=1.0).wait_for_completed()
        #move_lift(robot,-10,2)
        robot.drive_wheel_motors(-35,-35)
        time.sleep(2)
        robot.drive_wheel_motors(0,0)
        robot.set_lift_height(height=0.0).wait_for_completed()
        robot.drive_wheel_motors(-35,35)
        time.sleep(4)
        robot.drive_wheel_motors(0,0)
        #move_lift(robot,10,2)
        droppingBall = 0
        pickingBall = 0
        findingGoal = 0
    print("done droppingBall")    

###################################MAIN FUNCTION TO RUN PROGRAM#############################################
def cozmo_program(robot: cozmo.robot.Robot):
    global greenCounter
    global orangeCounter
    #global rect_cx
    #global rect_cy
    #global rect_w
    #global rect_h
    #global centered

    startedDriveThread = False
    robot.camera.color_image_enabled = True #turn on color
    robot.camera.image_stream_enabled = True #turn on camera feed

    time.sleep(2) #allow time to initialize, VERY IMPORTANT

    robot.set_lift_height(height=0.0).wait_for_completed()
    greenCounter = 0
    orangeCounter = 0
    #robot.set_head_angle(degrees(65),in_parallel=True)
    robot.move_head(-1)
    time.sleep(3)
    robot.move_head(0.75)
    time.sleep(0.6)
    robot.stop_all_motors()
    
    controlThread = threading.Thread(target=cozmoFindGreenBall, args=[robot,50,350])
    controlThread.start()

    while True: #loop images
        image = robot.world.latest_image.raw_image
        sharpened1 = image.filter(ImageFilter.SHARPEN);
        sharpened2 = sharpened1.filter(ImageFilter.SHARPEN);
        greenDrawBool, g_x, g_y, g_w, g_h, g_cx, g_cy = detectGreenBall(sharpened2)
        orangeDrawBool, o_x, o_y, o_w, o_h, o_cx, o_cy = detectOrangeTray(sharpened2)
        drawRectangles(sharpened2,greenDrawBool, g_x, g_y, g_w, g_h, g_cx, g_cy,orangeDrawBool, o_x, o_y, o_w, o_h, o_cx, o_cy)
        time.sleep(.003)
        greenCounter += 1
        orangeCounter += 1

    cv2.destroyAllWindows()

cozmo.run_program(cozmo_program)

