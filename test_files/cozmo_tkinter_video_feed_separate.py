#uses two different classes to separate the process of obtaining the image from cozmo and displaying it using tkinter
#using tkinter instead of opencv to display the cozmo view 
import cozmo
import cv2 
import time
import imutils
import numpy as np
from cozmo.util import degrees, distance_mm, speed_mmps
import threading
import tkinter as tk
from PIL import Image
from PIL import ImageTk

window = tk.Tk()

class CozmoReturnImage:
    def __init__(self, robot: cozmo.robot.Robot):
        robot.camera.color_image_enabled = True #turn on color
        robot.camera.image_stream_enabled = True #turn on camera feed
        print("initializing")
        time.sleep(2) 
              
    def cozmoGetImage(self,robot: cozmo.robot.Robot):
        image = robot.world.latest_image.raw_image 
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        frame = imutils.resize(frame, width=300)
        self.final_im = ImageTk.PhotoImage(image)
        return self.final_im
        time.sleep(.05) 

class TkinterDisplay(CozmoReturnImage):
    def __init__(self):
        self.canvas = tk.Canvas(window, width = 500, height = 500)
        self.canvas.pack()

    def displayFeed(self,robot: cozmo.robot.Robot):
        while True:
            self.canvas.create_image(20,20,anchor="nw",image=self.cozmoGetImage(robot))
            time.sleep(.05) 

def cozmo_program(robot: cozmo.robot.Robot):
    cozmoObj = CozmoReturnImage(robot)
    displayObj = TkinterDisplay()
    displayObj.displayFeed(robot)

if __name__ == "__main__":
    cozmoThread = threading.Thread(target=cozmo.run_program, args=[cozmo_program])
    cozmoThread.start()
    window.mainloop()
