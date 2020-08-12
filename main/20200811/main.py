#file imports
import turn_to_contour as turnToContour

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



############################## ORANGE GLOBAL VARIABLES ##############################
orangeLower = (0,135,140) #lower bound of HSV values for orange tray
orangeUpper = (24,210,255) #upper bound of HSV values for orange tray

orangeMinRectSize = 3000 #minimum size of rectangle to be drawn (if it is smaller, the function will not draw it)

orangeRect_x = 0 #The x coordinate of the top corner of the orange rectangle
orangeRect_y = 0 #The y coordinate of the top corner of the orange rectangle
orangeRect_h = 0 #height of the orange rectangle
orangeRect_w = 0 #width of the orange rectangle
orangeRect_cx = 0 #The x coordinate of the center of the orange rectangle
orangeRect_cy = 0 #The y coordinate of the center of the orange rectangle

############################## GREEN GLOBAL VARIABLES ##############################
greenLower = (47, 54, 10) #lower bound of HSV values for green ball
greenUpper = (80, 155, 150) #upper bound of HSV values for green ball

greenMinRectSize = 3000 #minimum size of rectangle to be drawn (if it is smaller, the function will not draw it)

greenRect_x = 0 #The x coordinate of the top corner of the green rectangle
greenRect_y = 0 #The y coordinate of the top corner of the green rectangle
greenRect_h = 0 #height of the green rectangle
greenRect_w = 0 #width of the green rectangle
greenRect_cx = 0 #The x coordinate of the center of the green rectangle
greenRect_cy = 0 #The y coordinate of the center of the green rectangle

############################## Picking & Dropping Balls Global Variables ##############################
pickingBall = 0
findingGoal = 0
droppingBall = 0

movingStraightSpeed = 20

repeatAttempts = 0


tolerance = 75 #tolerance for the amount of pixels the object can be off from the center of the camera
orangeRectWidthLimit = 1100
greenRectWidthLimit = 350


############################## OpenCV Functions ##############################

class Point: 
    #class to track the points of the orange and green bounding rectangles
    def __init__(self, x, y): 
        self.x = x 
        self.y = y
    
    def setCoordinates(self,x,y):
        self.x = x
        self.y = y

#make 4 point objects used to detect if the rectangles intersect each other
greenRectPointLeft = Point(0,0)
greenRectPointRight = Point(0,0)
orangeRectPointLeft = Point(0,0)
orangeRectPointRight = Point(0,0)

def doOverlap(l1, r1, l2, r2): 
    #returns true if rectangles overlap, uses Point class
    '''
    l1: Top Left coordinate of first rectangle.
    r1: Bottom Right coordinate of first rectangle.
    l2: Top Left coordinate of second rectangle.
    r2: Bottom Right coordinate of second rectangle.
    '''
    # If one rectangle is on left side of other 
    if(l1.x >= r2.x or l2.x >= r1.x): 
        return False
  
    # If one rectangle is above other 
    if(l1.y <= r2.y or l2.y <= r1.y): 
        return False
  
    return True

def detectGreenBall(image):
    #opencv function for
    global greenRect_x
    global greenRect_y
    global greenRect_h
    global greenRect_w
    global greenRect_cx
    global greenRect_cy
    
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=1280) #resize the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #convert frame to HSV

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
    
    if len(cnts) > 0:
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
        greenRectPointLeft.setCoordinates(x,y)
        greenRectPointRight.setCoordinates(int(x+w),int(y-h))
        greenRect_cx = x+(w/2.0)
        greenRect_cy = y+(h/2.0)
        
        if rect_area > greenMinRectSize:
            drawGreenRect = True
            cv2.rectangle(frame, (greenRect_x, greenRect_y) , (greenRect_x + greenRect_w, greenRect_y + greenRect_h) , (0,0,0) , 3)
            cv2.line(frame, (int(greenRect_cx), int(greenRect_cy)), (int(greenRect_cx), int(greenRect_cy)), (255, 0, 0), thickness=10)

    elif len(cnts) == 0 or rect_area < greenMinRectSize: #if there is no contour or if the contour is too small set the variables to None
        greenRect_cx = None
        greenRect_w = None
        greenRect_h = None
    
    return drawGreenRect,greenRect_x,greenRect_y,greenRect_w,greenRect_h,greenRect_cx,greenRect_cy #return these values to draw with drawing function

def detectOrangeTray(image):
    global orangeRect_x
    global orangeRect_y
    global orangeRect_h
    global orangeRect_w
    global orangeRect_cx
    global orangeRect_cy
    
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=1280) #resize the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #change from BGR to HSV

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

    drawOrangeRect = False #boolean value to see in the rectangle is large enough to be drawn
    
    if len(cnts) > 0:
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
        orangeRectPointLeft.setCoordinates(x,y)
        orangeRectPointRight.setCoordinates(int(x+w),int(y-h))
        orangeRect_cx = x+(w/2.0)
        orangeRect_cy = y+(h/2.0)
        
        if rect_area > orangeMinRectSize:
            drawOrangeRect = True
            cv2.rectangle(frame, (orangeRect_x, orangeRect_y) , (orangeRect_x + orangeRect_w, orangeRect_y + orangeRect_h) , (0,0,0) , 3)
            cv2.line(frame, (int(orangeRect_cx), int(orangeRect_cy)), (int(orangeRect_cx), int(orangeRect_cy)), (255, 0, 0), thickness=10)

    elif len(cnts) == 0 or rect_area < orangeMinRectSize: #if there is no contour or if the contour is too small set the variables to None
        orangeRect_cx = None
        orangeRect_w = None
        orangeRect_h = None
             
    return drawOrangeRect,orangeRect_x,orangeRect_y,orangeRect_w,orangeRect_h,orangeRect_cx,orangeRect_cy #return these values to draw with drawing function


def drawRectangles(image, greenDrawBool, g_x, g_y, g_w, g_h, g_cx, g_cy, orangeDrawBool, o_x, o_y, o_w, o_h, o_cx, o_cy):
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=1280)   
    
    if greenDrawBool: #draws if the green rectangle is large enough
        cv2.rectangle(frame, (g_x, g_y) , (g_x + g_w, g_y + g_h) , (0,255,0) , 3)
        cv2.line(frame, (int(g_cx), int(g_cy)), (int(g_cx), int(g_cy)), (255, 0, 0), thickness=10)
        
    if orangeDrawBool: #draws if the orange rectangle is large enough
        cv2.rectangle(frame, (o_x, o_y) , (o_x + o_w, o_y + o_h) , (0,0,255) , 3)
        cv2.line(frame, (int(o_cx), int(o_cy)), (int(o_cx), int(o_cy)), (255, 0, 0), thickness=10)
        
    cv2.imshow('image', frame)
    key = cv2.waitKey(1) & 0xFF
 
 
 
############################## Cozmo Movement Functions ##############################
def cozmo_get_speed(color):  
    #function to get an appropriate speed based on how far the object is from the center of the cozmo's camera  
    global greenRect_cx
    global greenRect_cy
    global orangeRect_cx
    global orangeRect_cy
    
    speed = 0
    if color == "green": # green
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
    elif color == "orange": # orange
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
    
def cozmoFindGreenBall(robot: cozmo.robot.Robot):
    #function for moving until a green ball is in the center of the camera
    global greenRect_cx
    global greenRect_w
    global movingStraightSpeed
    
    global pickingBall
    global findingGoal
    global droppingBall
        
    global tolerance
    global greenRectWidthLimit

    global repeatAttempts
    
    turntodirection_green = 0
    
    upperLimit = 640 + tolerance
    lowerLimit = 640 - tolerance
        
    while pickingBall == 0 and findingGoal == 0 and droppingBall == 0:
        speed = cozmo_get_speed("green") #gets proportional speed
        
        if turntodirection_green == 0: #this variable makes sure the turn_to_direction code runs only once
            turnToContour.turn_to_direction(robot,"green") #first turns to the general direction of the contour
            turntodirection_green = 1

        #print(greenRect_w)
        if greenRect_cx != None: #if the cozmo sees a green ball somewhere in the frame
            if not doOverlap(greenRectPointLeft,greenRectPointRight,orangeRectPointLeft,orangeRectPointRight): #makes sure that the rectangles do not overlap before picking
                if greenRect_cx > upperLimit:
                    robot.drive_wheel_motors(speed, 0 ) #-speed
                if greenRect_cx < lowerLimit:
                    robot.drive_wheel_motors( 0 , speed) #-speed
                if greenRect_cx < upperLimit and greenRect_cx > lowerLimit: #when the robot is greenCentered on a ball, start moving towards it
                    speed = cozmo_get_speed("green")
                    if greenRect_w < greenRectWidthLimit:
                        robot.drive_wheel_motors(movingStraightSpeed,movingStraightSpeed) #drive forward if rectangle is too small

                    elif greenRect_w > greenRectWidthLimit + 50:
                        robot.drive_wheel_motors(-movingStraightSpeed,-movingStraightSpeed) #back up if rectangle is too big
       
                    else:
                        robot.drive_wheel_motors(0,0)
                        pick_ball(robot)
                        turntodirection_green = 0 #resets variable so after the picking and dropping ball sequence has occured, the turn_to_direction function can run again 
                        
            else: #reset variables so the robot goes back to look for a different ball
                #robot.say_text("Ball was already picked").wait_for_completed()
                droppingBall = 0
                pickingBall = 0
                findingGoal = 0
                
                repeatAttempts += 1 #if the robot tries to pick a ball in the goal, add to the repeat attempts counter. If this counter reaches 3, the program terminates
                
                robot.drive_wheel_motors(-movingStraightSpeed,-movingStraightSpeed)
                time.sleep(1)
                robot.drive_wheel_motors(0,0)
                
                turnToContour.turn_to_direction(robot,"green") #reruns find contour function to try and get a different green ball
                
        else:
            turnToContour.turn_to_direction(robot,"green") #reruns find contour function to try and get the green ball in a general area
    
def pick_ball(robot: cozmo.robot.Robot):
    #function for picking the ball, it follows detectGreenBall (after the green ball is in the center of the camera)
    global pickingBall
    
    speed = 35
    pickingBall = 1
    
    if pickingBall == 1:
        robot.set_lift_height(height=1.0).wait_for_completed()
        robot.drive_wheel_motors(speed,speed)
        time.sleep(2)
        robot.drive_wheel_motors(0,0) 
        robot.set_lift_height(height=0.0).wait_for_completed()
        robot.drive_wheel_motors(speed,speed)
        time.sleep(2)
        robot.drive_wheel_motors(0,0)
        robot.set_lift_height(height=1.0).wait_for_completed()
        pickingBall = 2
        
        find_goal(robot)
        

def find_goal(robot: cozmo.robot.Robot):
    #code for moving towards the orange tray
    global pickingBall
    global findingGoal
    global droppingBall
    global movingStraightSpeed
    
    global orangeRect_cx
    global orangeRect_w
    
    global tolerance
    global orangeRectWidthLimit
    
    turntodirection_orange = 0
    
    upperLimit = 640 + (tolerance + 25)
    lowerLimit = 640 - (tolerance + 25)

    findingGoal = 1
    
    while pickingBall == 2 and findingGoal == 1 and droppingBall == 0: # if ball has been picked update
        speed = cozmo_get_speed("orange")
        
        if turntodirection_orange == 0: #this variable makes sure the turn_to_direction code runs only once
            turnToContour.turn_to_direction(robot, "orange") #turns to the general direction of the orange contour
            turntodirection_orange = 1
        
        if orangeRect_cx != None:
            if orangeRect_cx > upperLimit:
                robot.drive_wheel_motors(speed, 0 ) #-speed
            if orangeRect_cx < lowerLimit:
                robot.drive_wheel_motors( 0 , speed) #-speed
            if orangeRect_cx < upperLimit and orangeRect_cx > lowerLimit: #when the robot is orangeCentered on a ball, start moving towards it
                speed = cozmo_get_speed("orange")
                if orangeRect_w < orangeRectWidthLimit:
                    robot.drive_wheel_motors(movingStraightSpeed,movingStraightSpeed) #move forward if rectangle is too small
                elif orangeRect_w > orangeRectWidthLimit + 50:
                    robot.drive_wheel_motors(-movingStraightSpeed,-movingStraightSpeed) #back up if rectangle is too big
                else:
                    robot.drive_wheel_motors(0,0)
                    findingGoal = 0
                    turntodirection_orange = 0
                    drop_ball(robot)
        
        else:
            turnToContour.turn_to_direction(robot, "orange") #if the robot cannot see an orange contour, run this function to try and find one
    
def drop_ball(robot: cozmo.robot.Robot):
    #function for dropping the ball, it follows find_goal (after the orange tray is in the center of the camera)
    global droppingBall
    global pickingBall
    global findingGoal
    
    droppingBall = 1
    speed = 35
    
    if droppingBall == 1 and findingGoal == 0:
        robot.drive_wheel_motors(speed,speed) #have to move robot forward more in order to drop the ball in 
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
        
        #resetting variables so the cycle can continue
        droppingBall = 0
        pickingBall = 0
        findingGoal = 0


        

############################## Main Function to Run Program ##############################
def cozmo_program(robot: cozmo.robot.Robot):
    global repeatAttempts

    startedDriveThread = False
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
        
    controlThread = threading.Thread(target=cozmoFindGreenBall, args=[robot])
    controlThread.start()
    
    while True: #loop images
        image = robot.world.latest_image.raw_image
        sharpened1 = image.filter(ImageFilter.SHARPEN);
        sharpened2 = sharpened1.filter(ImageFilter.SHARPEN);
        greenDrawBool, g_x, g_y, g_w, g_h, g_cx, g_cy = detectGreenBall(sharpened2)
        orangeDrawBool, o_x, o_y, o_w, o_h, o_cx, o_cy = detectOrangeTray(sharpened2)
        drawRectangles(sharpened2,greenDrawBool, g_x, g_y, g_w, g_h, g_cx, g_cy,orangeDrawBool, o_x, o_y, o_w, o_h, o_cx, o_cy)
        #time.sleep(.003)
        if repeatAttempts >= 3: #if the robot tries to pick up a ball that is already in the goal 3 times, exit out of the program
            robot.say_text("Tried to pick up a ball that was in the goal more than 3 times, terminating program.",play_excited_animation=False).wait_for_completed()
            break
            
    print("Picking Balls Completed")
    robot.say_text("Done!!!",play_excited_animation=True).wait_for_completed()

    cv2.destroyAllWindows()

cozmo.run_program(cozmo_program)

