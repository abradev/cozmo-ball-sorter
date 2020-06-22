import cozmo
import cv2 
import time
import imutils
import numpy as np
from cozmo.util import degrees, distance_mm, speed_mmps


def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",35,255,empty)
cv2.createTrackbar("Threshold2","Parameters",45,255,empty)

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            cv2.drawContours(imgContour,cnt,-1,(255,0,255),7)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w, y+h), (0,255,0), 5)
def cozmo_program(robot: cozmo.robot.Robot):
    robot.camera.color_image_enabled = True #turn on color
    robot.camera.image_stream_enabled = True #turn on camera feed

    time.sleep(2) #allow time to initialize, VERY IMPORTANT
    while True: #loop images
        image = robot.world.latest_image.raw_image 
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (640, 480))
        imgContour = frame.copy()
        
        imgBlur = cv2.GaussianBlur(frame,(7,7),1)
        imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)

        threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
        threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")
        imgCanny = cv2.Canny(imgGray,threshold1,threshold2)
        kernel = np.ones((5,5))
        imgDil = cv2.dilate(imgCanny,kernel,iterations=1)
        getContours(imgDil,imgContour)
        
        
        cv2.imshow("canny image",imgContour)
        cv2.imshow("camera feed",frame)
        
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
        #key = cv2.waitKey(1) & 0xFF
        
        time.sleep(.05)

    cv2.destroyAllWindows()

cozmo.run_program(cozmo_program)
