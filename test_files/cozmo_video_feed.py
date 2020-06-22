import cozmo
import cv2 
import time
import imutils
import numpy as np
from cozmo.util import degrees, distance_mm, speed_mmps

def cozmo_program(robot: cozmo.robot.Robot):
    robot.camera.color_image_enabled = True #turn on color
    robot.camera.image_stream_enabled = True #turn on camera feed

    time.sleep(2) #allow time to initialize, VERY IMPORTANT
    while True: #loop images
        image = robot.world.latest_image.raw_image 
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (640, 480))
        cv2.imshow("camera image",frame)
        key = cv2.waitKey(1) & 0xFF
        time.sleep(.05)

    cv2.destroyAllWindows()

cozmo.run_program(cozmo_program)
