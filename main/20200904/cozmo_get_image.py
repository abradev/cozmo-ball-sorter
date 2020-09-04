import cozmo
import numpy as np
from PIL import Image, ImageTk, ImageFilter
import cv2
from time import sleep

import config as CONFIG

class CozmoReturnImage:
    def __init__(self, robot: cozmo.robot.Robot):
        robot.camera.color_image_enabled = True #turn on color
        robot.camera.image_stream_enabled = True #turn on camera feed
        print("initializing")
        time.sleep(2) 
              
    def cozmoGetImage(self,robot: cozmo.robot.Robot, get_cv2_image=False):
        image = robot.world.latest_image.raw_image
        sharpened1 = image.filter(ImageFilter.SHARPEN)
        npImage = np.array(sharpened1)
        #print(npImage.shape[0])
        #print(npImage.shape[1])
        bgrImage = cv2.cvtColor(npImage, cv2.COLOR_RGB2BGR)
        hsvImage = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2HSV)
        self.resizedImage = cv2.resize(hsvImage, dsize=(CONFIG.frameWidth, CONFIG.frameHeight), interpolation=cv2.INTER_CUBIC) 
        self.final_im = ImageTk.PhotoImage(Image.fromarray(self.resizedImage))
        if get_cv2_image:
            return  self.resizedImage
        else:
            return self.final_im
        time.sleep(CONFIG.refreshTime)

    def cozmoReturnImage(self, robot: cozmo.robot.Robot):
        while True:
            CONFIG.img_cozmo = self.cozmoGetImage(robot)