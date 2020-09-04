import cozmo
from cozmo.util import *

from cv2 import cv2
import PIL
from PIL import ImageFilter
import imutils
import numpy as np

from shapely.geometry import Point, Polygon

import time
import threading
import psutil

#import cozmo_gui
#import turn_to_contour
#import config

class Point: 
    #class to track the points of the orange and green bounding rectangles
    def __init__(self, x, y): 
        self.x = x 
        self.y = y
    
    def setCoordinates(self,x,y):
        self.x = x
        self.y = y

    def overlap(self, comparingRectangle): 
        #returns true if rectangles overlap, uses Point class
        '''
        l1: Top Left coordinate of first rectangle.
        r1: Bottom Right coordinate of first rectangle.
        l2: Top Left coordinate of second rectangle.
        r2: Bottom Right coordinate of second rectangle.
        '''
        # If one rectangle is on left side of other 
        if(self.l1.x >= r2.x or l2.x >= r1.x): 
            return False
    
        # If one rectangle is above other 
        if(l1.y <= r2.y or l2.y <= r1.y): 
            return False
        
        return True
  

class VarsInit:
    def __init__(self):
        self.ballColorList = []
        self.trayColorList = []
        self.trayRectVars = []
        self.ballRectVars = []
        self.trayRectPoints = []
        self.ballRectPoints = []

    def append_color(self, objectType, colorTuple): #add a colorrange
        if objectType == "ball":
            self.ballColorList.append(colorTuple)
        elif objectType == "tray":
            self.trayColorList.append(colorTuple)

    def delete_color(self, objectType, colorIndex): #delete a colorrange
        if objectType == "ball":
            self.ballColorList.pop(colorIndex)
        elif objectType == "tray":
            self.trayColorList.pop(colorIndex)

    def init_vars(): #reinitializes rectangle variables for the different objects
        self.trayRectVars.clear()
        self.ballRectVars.clear()
        self.trayRectPoints.clear()
        self.ballRectPoints.clear()

        for i in range(ballColorList):
            self.ballRectVars.append((False,0,0,0,0,0,0))
            self.ballRectPoints.append((Point(0,0),Point(0,0))) #append 2 points as a tuple to index in list

        for j in range(trayColorList):
            self.trayRectVars.append((False,0,0,0,0,0,0))
            self.trayRectPoints.append((Point(0,0),Point(0,0))) #append 2 points as a tuple to index in list

def detectTray(image):
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=1280) #resize the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert frame to HSV

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    for colorRange in trayColorList:
        mask = cv2.inRange(hsv, colorRange[0], colorRange[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # only proceed if at least one contour was found

        drawRect = False #boolean value to see in the rectangle is large enough
        
        if len(cnts) > 0:
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
            rect_area = w * h
            trayRectPoints[i][0].setCoordinates(x,y)
            trayRectPoints[i][1].setCoordinates(int(x+w),int(y-h))
            rect_cx = x+(w/2.0)
            rect_cy = y+(h/2.0)
            
            if rect_area > trayMinWidth:
                drawRect = True
                #cv2.rectangle(frame, (rect_x, rect_y) , (rect_x + rect_w, rect_y + rect_h) , (0,0,0) , 3)
                #cv2.line(frame, (int(rect_cx), int(rect_cy)), (int(rect_cx), int(rect_cy)), (255, 0, 0), thickness=10)

        elif len(cnts) == 0 or rect_area < trayMinWidth: #if there is no contour or if the contour is too small set the variables to None
            rect_cx = None
            rect_w = None
            rect_h = None
        
        trayRectVars[i] = (drawRect,rect_x,rect_y,rect_w,rect_h,rect_cx,rect_cy)

    config.biggestTray = 0
    counter = 0
    for rectVar in trayRectVars:
        if rectVar[3]*rectVar[4] > config.biggestTray:
            config.biggestTray = counter
        counter += 1
    return config.biggestTray

def detectBall(image): 
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=1280) #resize the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert frame to HSV

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    for colorRange in ballColorList:
        mask = cv2.inRange(hsv, colorRange[0], colorRange[1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # only proceed if at least one contour was found

        drawRect = False #boolean value to see in the rectangle is large enough
        
        if len(cnts) > 0:
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
            rect_area = w * h
            ballRectPoints[i][0].setCoordinates(x,y)
            ballRectPoints[i][1].setCoordinates(int(x+w),int(y-h))
            rect_cx = x+(w/2.0)
            rect_cy = y+(h/2.0)
            
            if rect_area > ballMinWidth:
                drawRect = True
                #cv2.rectangle(frame, (rect_x, rect_y) , (rect_x + rect_w, rect_y + rect_h) , (0,0,0) , 3)
                #cv2.line(frame, (int(rect_cx), int(rect_cy)), (int(rect_cx), int(rect_cy)), (255, 0, 0), thickness=10)

        elif len(cnts) == 0 or rect_area < ballMinWidth: #if there is no contour or if the contour is too small set the variables to None
            rect_cx = None
            rect_w = None
            rect_h = None
        
        ballRectVars[i] = (drawRect,rect_x,rect_y,rect_w,rect_h,rect_cx,rect_cy)

    config.biggestBall = 0
    counter = 0
    for rectVar in ballRectVars:
        if rectVar[3]*rectVar[4] > config.biggestBall:
            config.biggestBall = counter
        counter += 1
    return config.biggestBall

def drawRectangles(image):
    config.biggestBall = detectBall(image)
    config.biggestTray = detectTray(image)

    frame = image
    #frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    #frame = imutils.resize(frame, width=1280)   
    
    ball = ballRectVars[config.biggestBall]
    ball_drawRect = ball[0]
    ball_x = ball[1]
    ball_y = ball[2]
    ball_w = ball[3]
    ball_h = ball[4]
    ball_cx = ball[5]
    ball_cy = ball[6]

    if ball_drawRect: #draws if the green rectangle is large enough
        cv2.rectangle(frame, (ball_x, ball_y) , (ball_x + ball_w, ball_y + ball_hg_h) , (0,255,0) , 3)
        cv2.line(frame, (int(ball_cx), int(ball_cy)), (int(ball_cx), int(ball_cy)), (255, 0, 0), thickness=10)

    tray = trayRectVars[config.biggestTray]
    tray_drawRect = tray[0]
    tray_x = tray[1]
    tray_y = tray[2]
    tray_w = tray[3]
    tray_h = tray[4]
    tray_cx = tray[5]
    tray_cy = tray[6]

    if tray_drawRect: #draws if the orange rectangle is large enough
        cv2.rectangle(frame, (tray_x, tray_y) , (tray_x + tray_w, tray_y + tray_h) , (0,0,255) , 3)
        cv2.line(frame, (int(tray_cx), int(tray_cy)), (int(tray_cx), int(tray_cy)), (255, 0, 0), thickness=10)
        
    return frame

class CozmoMovement(VarsInit):
    def __init__(self, robot: cozmo.robot.Robot):
        robot.camera.color_image_enabled = True #turn on color
        robot.camera.image_stream_enabled = True #turn on camera feed
        time.sleep(2) #allow time to initialize, VERY IMPORTANT

        robot.set_lift_height(height=0.0).wait_for_completed()

        #initial movements for configuring the Cozmo
        robot.move_head(-1)
        time.sleep(3)
        robot.move_head(0.75)
        time.sleep(0.6)
        robot.stop_all_motors()

        self.speed = 10

    def findSpeed(self, objectType):
        if objectType == "ball":
            self.speed = 10
        elif objectType == "tray":
            self.speed = 10

    def findBiggest(self,objectType):
        config.biggestBall = 0
        config.biggestTray = 0

        if objectType == "ball":
            for i in range(len(self.ballRectVars)):
                if self.ballRectVars[i][3]*self.ballRectVars[i][4] > config.biggestBall:
                    config.biggestBall = i
            return config.biggestBall

        elif objectType == "tray":
            for i in range(len(self.trayRectVars)):
                if self.trayRectVars[i][3]*self.trayRectVars[i][4] > config.biggestTray:
                    config.biggestTray = i
            return config.biggestTray

    def findObj(self, objectType):
        ballDictNum = 0
        trayDictNum = 0
        speed = 0
        rect_w = 0
        rect_cx = 0
        rectWidthMinimum = 0

        if objectType == "ball":
            rectWidthMinimum = config.ballMinWidth
            ballDictNum = self.findBiggest(objectType)
            trayDictNum = self.findBiggest("tray")
            ball_turnToDirection = 0
            upperLimit = config.centerOfFrame + config.ballTolerance
            lowerLimit = config.centerOfFrame - config.ballTolerance

            while config.moveCozmo:
                rect_w = self.ballRectVars[ballDictNum][3]
                rect_cx = self.ballRectVars[ballDictNum][5]
                speed = self.findSpeed(objectType)
                if ball_turnToDirection == 0: #this variable makes sure the turn_to_direction code runs only once
                    turnToContour.turn_to_direction(robot,objectType) #first turns to the general direction of the contour
                    ball_turnToDirection = 1

                #print(greenRect_w)
                if rect_cx != None: #if the cozmo sees a green ball somewhere in the frame
                    if not ballRectPoints[ballDictNum].overlap(trayRectPoints[trayDictNum]):
                    #if not doOverlap(ballRectPointLeft,ballRectPointRight,trayRectPointLeft,trayRectPointRight): #makes sure that the rectangles do not overlap before picking
                        if rect_cx > upperLimit:
                            robot.drive_wheel_motors(speed, 0 ) #-speed
                        if rect_cx < lowerLimit:
                            robot.drive_wheel_motors( 0 , speed) #-speed
                        if rect_cx < upperLimit and rect_cx > lowerLimit: #when the robot is greenCentered on a ball, start moving towards it
                            speed = cozmo_get_speed(objectType)
                            if rect_w < ballMinWidth:
                                robot.drive_wheel_motors(config.movingStraightSpeed,config.movingStraightSpeed) #drive forward if rectangle is too small

                            elif greenRect_w > greenRectWidthLimit + 50:
                                robot.drive_wheel_motors(-config.movingStraightSpeed,-config.movingStraightSpeed) #back up if rectangle is too big
            
                            else:
                                robot.drive_wheel_motors(0,0)
                                self.pickBall()
                                ball_turnToDirection = 0 #resets variable so after the picking and dropping ball sequence has occured, the turn_to_direction function can run again 
                                
                    else: #reset variables so the robot goes back to look for a different ball
                        #robot.say_text("Ball was already picked").wait_for_completed()
                        config.repeatAttempts += 1 #if the robot tries to pick a ball in the goal, add to the repeat attempts counter. If this counter reaches 3, the program terminates
                        
                        robot.drive_wheel_motors(-config.movingStraightSpeed,-config.movingStraightSpeed)
                        time.sleep(1)
                        robot.drive_wheel_motors(0,0)
                        
                        turnToContour.turn_to_direction(robot,objectType) #reruns find contour function to try and get a different green ball
                        
                else:
                    turnToContour.turn_to_direction(robot,objectType) #reruns find contour function to try and get the green ball in a general area
    
        elif objectType == "tray":
            rectWidthMinimum = config.trayMinWidth
            trayDictNum = self.findBiggest(objectType)
            tray_turnToDirection = 0
            upperLimit = config.centerOfFrame + config.trayTolerance
            lowerLimit = config.centerOfFrame - config.trayTolerance
            while config.moveCozmo:
                rect_w = self.trayRectVars[trayDictNum][3]
                rect_cx = self.trayRectVars[trayDictNum][5]
                speed = self.findSpeed(objectType)
                if tray_turnToDirection == 0: #this variable makes sure the turn_to_direction code runs only once
                    turnToContour.turn_to_direction(robot,objectType) #turns to the general direction of the orange contour
                    tray_turnToDirection = 1
                
                if rect_cx != None:
                    if rect_cx > upperLimit:
                        robot.drive_wheel_motors(speed, 0 ) #-speed
                    if rect_cx < lowerLimit:
                        robot.drive_wheel_motors( 0 , speed) #-speed
                    if rect_cx < upperLimit and rect_cx > lowerLimit: #when the robot is orangeCentered on a ball, start moving towards it
                        speed = cozmo_get_speed(objectType)
                        if rect_w < trayMinWidth:
                            robot.drive_wheel_motors(config.movingStraightSpeed,config.movingStraightSpeed) #move forward if rectangle is too small
                        elif rect_w > trayMinWidth + 50:
                            robot.drive_wheel_motors(-config.movingStraightSpeed,-config.movingStraightSpeed) #back up if rectangle is too big
                        else:
                            robot.drive_wheel_motors(0,0)
                            tray_turnToDirection = 0
                            self.dropBall()
                
                else:
                    turnToContour.turn_to_direction(robot, objectType) #if the robot cannot see an orange contour, run this function to try and find one
            
    def pickBall(self):
        robot.set_lift_height(height=1.0).wait_for_completed()
        robot.drive_wheel_motors(speed,speed)
        time.sleep(2)
        robot.drive_wheel_motors(0,0) 
        robot.set_lift_height(height=0.0).wait_for_completed()
        robot.drive_wheel_motors(speed,speed)
        time.sleep(2)
        robot.drive_wheel_motors(0,0)
        robot.set_lift_height(height=1.0).wait_for_completed()
        self.findObj("tray")

    def dropBall(self):
        robot.drive_wheel_motors(speed,speed)
        time.sleep(3)
        robot.drive_wheel_motors(0,0)
        robot.set_lift_height(height=0.25).wait_for_completed()
        robot.drive_wheel_motors(-speed,-speed)
        time.sleep(1.5)
        robot.drive_wheel_motors(0,0) 
        robot.set_lift_height(height=1.0).wait_for_completed()
        robot.drive_wheel_motors(-speed,-speed)
        time.sleep(3)
        robot.drive_wheel_motors(0,0)
        robot.set_lift_height(height=0.0).wait_for_completed()
        robot.drive_wheel_motors(-speed,speed)
        time.sleep(4)
        robot.drive_wheel_motors(0,0)
        self.findObj("ball")

def cozmo_program():
    varInitializer = VarsInit()
    varInitializer.append_color("ball",((0,0,0),(0,0,0)))
    varInitializer.append_color("tray",((0,0,0),(0,0,0)))
    varInitializer.init_vars()
    cozmoRobot = cozmoMovement(robot)
    cozmoMoveThread = psutil.Process(target=cozmoRobot.findObj,args="ball")
    cozmoMoveThread.start()

    while True:
        cozmoDetect.drawRectangles(image)
        time.sleep(0.05)

