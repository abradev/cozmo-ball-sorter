#import cozmo_gui as CG
import config as CONFIG

import cozmo_detect as F_COZMO_DETECT
import cozmo_movement as F_COZMO_MOVEMENT
import cozmo_find_contour as F_COZMO_FIND_CONTOUR
import cozmo_gui as F_COZMO_GUI
import cozmo_get_image as F_COZMO_GET_IMAGE

import cozmo

from time import sleep
from multiprocessing import Process
import psutil

def ImageSetter():
    cozmoImageGetter = F_COZMO_GET_IMAGE.CozmoReturnImage(CONFIG.ROBOT)
    cozmoImageGetter.cozmoReturnImage(CONFIG.ROBOT)

def test():
    varInitializer = F_COZMO_MOVEMENT.VarsInit()
    varInitializer.append_color("ball",((0,0,0),(0,0,0)))
    varInitializer.append_color("tray",((0,0,0),(0,0,0)))
    varInitializer.init_vars()



def detect():
    while True:
        F_COZMO_DETECT.drawRectangles(CONFIG.img_cozmo)
        time.sleep(0.05)

def ProcessChecker():
    #process used to check for the state of certain variables
    imageSetterProcess = Process(target=ImageSetter)
    imageSetterProcess.start()

    cozmoRobot = F_COZMO_MOVEMENT.CozmoMovement(CONFIG.ROBOT)
    cozmoMoveProcess = Process(target=cozmoRobot.findObj,args="ball")
    cozmoMoveProcess.start()

    #cozmoMoveProcess = Process(target = )
    #cozmoMoveProcess.start()

    psutil_cozmoMoveProcess = psutil.Process(cozmoMoveProcess.pid) #need to have a psutil version of the process in order to pause

    while True:
        if CONFIG.cozmo_move == False: #if the variable says not to move the cozmo, stop the process
            psutil_cozmoMoveProcess.suspend()
        else:
            psutil_cozmoMoveProcess.resume()
            
def cozmo_program(robot: cozmo.robot.Robot):
    CONFIG.ROBOT = robot

    processChecker = Process(target=ProcessChecker) #starts all the processes, and also is able to pause/resume them
    processChecker.start()

    cozmoObj = CozmoReturnImage(robot)
    setColorsThread = threading.Thread(target=gui.setColorsObj.displayFeed, args=[robot]) #start cozmo video feed for setcolorspage
    setColorsThread.start()
    cozmoProcessImageThread = threading.Thread(target=cozmoProcessImage, args=[cozmoObj.cozmoGetImage(robot),robot])
    cozmoProcessImageThread.start()
    gui.findBallsObj.displayFeed(robot) #start cozmo video feed for findingballspage

    print("hello")

if __name__ == "__main__":
    #cozmo.run_program(cozmo_program)
    gui = F_COZMO_GUI.GUI()
    gui.wm_geometry("800x800+300+100")
    cozmoProcess = Process(target=cozmo.run_program, args=[cozmo_program])
    cozmoProcess.start()
    gui.mainloop()
    
