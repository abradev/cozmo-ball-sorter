try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2
import cozmo
import cv2 
import time
import threading
from functools import partial
import imutils
import numpy as np
from cozmo.util import degrees, distance_mm, speed_mmps
from PIL import Image
from PIL import ImageTk
from PIL import ImageFilter
import config

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.titleFont = tkfont.Font(family='Fixedsys', size=50)
        self.subtitleFont = tkfont.Font(family='Fixedsys', size=20)
        self.buttonFont = tkfont.Font(family='Fixedsys', size=12)
        self.textFont = tkfont.Font(family='Fixedsys', size=12)
        self.iconFont = tkfont.Font(family='Fixedsys', size=50)
        self.buttonHeight = 2
        self.buttonWidth = 25

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.parentHolder = container
        self.controllerHolder = self

        self.frames = {}
        i = 0
        for F in (HomePage, TutorialPage, AboutPage, SetColorsPage, FindingBallsPage, ErrorPage, ProgramTerminatedPage): #Namse of all the pages
            i+=1
            if i==4: #setcolorspage index
                page_name = F.__name__
                self.setColorsObj = SetColorsPage(parent=container, controller=self)
                #self.setColorsObj.displayFeed(robot)
                self.frames[page_name] = self.setColorsObj
                self.setColorsObj.grid(row=0, column=0, sticky="nsew")

            elif i==5: #findingballspage index
                page_name = F.__name__
                self.findBallsObj = FindingBallsPage(parent=container,controller=self)
                self.frames[page_name] = self.findBallsObj
                self.findBallsObj.grid(row=0,column=0,sticky="nsew")

            else:   
                page_name = F.__name__
                frame = F(parent=container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.configure(bg="white")
        frame.tkraise()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="COZMO", font=controller.titleFont,bg="white")
        title.pack()
        subtitle = tk.Label(self,text="Ball Picker", font=controller.subtitleFont, bg="white")
        subtitle.pack()
        
        space1 = tk.Label(self,bg="white")
        space1.pack()

        button1 = tk.Button(self, text="continue", bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=controller.buttonWidth, command=lambda: controller.show_frame("SetColorsPage"))
        button2 = tk.Button(self, text="tutorial", bg="white", font=controller.buttonFont,height=controller.buttonHeight, width=controller.buttonWidth, command=lambda: controller.show_frame("TutorialPage"))
        button3 = tk.Button(self, text="about", bg="white",  font=controller.buttonFont,height=controller.buttonHeight, width=controller.buttonWidth, command=lambda: controller.show_frame("AboutPage"))
        button1.pack()
        button2.pack()
        button3.pack()


class TutorialPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        text = tk.Label(self, text="Video for the tutorial will go here", bg="white",font=controller.textFont)
        text.pack()
        space1 = tk.Label(self,bg="white")
        space1.pack()
        button = tk.Button(self, text="back", bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=controller.buttonWidth, command=lambda: controller.show_frame("HomePage"))
        button.pack()


class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        space1 = tk.Label(self,bg="white")
        space1.pack()
        aboutBullet1 = tk.Label(self, text="•The Cozmo Ball Sorter is a project that enables the Anki Cozmo to be placed in an environment of different colored balls and systematically deposit them in designated areas",font=controller.textFont,wraplength=300,justify="left",bg="white")
        aboutBullet1.pack()
        aboutBullet2 = tk.Label(self, text="•Using OpenCV to process images from the Cozmo, the program detects the balls and returns a coordinate to make the robot turn towards the ball",font=controller.textFont,wraplength=300,justify="left",bg="white")
        aboutBullet2.pack()
        aboutBullet3 = tk.Label(self, text="•This project was started in May 2020 by Kathline Newland and Jeremy Dapaah",font=controller.textFont,wraplength=300,justify="left",bg="white")
        aboutBullet3.pack()
        space2 = tk.Label(self,bg="white")
        space2.pack()
        link = tk.Label(self,text="Visit our Github repository to see the code for this project: [add link here] ",font=controller.textFont,bg="white",wraplength=300)
        link.pack()
        space3 = tk.Label(self,bg="white")
        space3.pack()
        button = tk.Button(self, text="back", bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=controller.buttonWidth, command=lambda: controller.show_frame("HomePage"))
        button.pack()

class CozmoReturnImage:
    def __init__(self, robot: cozmo.robot.Robot):
        robot.camera.color_image_enabled = True #turn on color
        robot.camera.image_stream_enabled = True #turn on camera feed
        print("initializing")
        time.sleep(2) 
              
    def cozmoGetImage(self,robot: cozmo.robot.Robot):
        image = robot.world.latest_image.raw_image
        sharpened1 = image.filter(ImageFilter.SHARPEN)
        npImage = np.array(sharpened1)
        #print(npImage.shape[0])
        #print(npImage.shape[1])
        resizedImage = cv2.resize(npImage, dsize=(600, 450), interpolation=cv2.INTER_CUBIC) 
        self.final_im = ImageTk.PhotoImage(Image.fromarray(resizedImage))
        return self.final_im
        time.sleep(config.refreshTime)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
ballColorEntries = 0
trayColorEntries = 0
ballColorDict = {}
trayColorDict = {}

def returnStr(string,value):
    return str(string+str(value))

def enterColorIntoList(listType,frame, upperColor, lowerColor):
    global ballColorEntries
    global trayColorEntries
    #global ballColorDict

    if listType == "ballColorDict":
        ballColorDict[returnStr("ballColor_",ballColorEntries)] = tk.Label(frame, text = "Lower Bound: " + str(lowerColor) + ", Upper Bound: " + str(upperColor), font=("Fixedsys",15), wraplength=100).pack()
        ballColorEntries += 1
    else:
        trayColorDict[returnStr("trayColor_",trayColorEntries)] = tk.Label(frame, text = "Lower Bound: " + str(lowerColor) + ", Upper Bound: " + str(upperColor), font=("Fixedsys",15), wraplength=100).pack()
        trayColorEntries += 1
    return 0

def deleteColorFromList(listType,frame,index):
    global ballColorEntries
    global trayColorEntries
    #global ballColorDict
    if listType == "ballColorDict":
        ballColorDict.get(returnStr("ballColor_",index)).destroy().pack()
        del ballColorDict[returnStr("ballColor_",index)]
    else:
        del trayColorDict[returnStr("trayColor_",index)]
    #enterColorIntoList(frame_0_0, "44,23,9", "23,88,54")

class SetColorsPage(tk.Frame, CozmoReturnImage):
    '''This page is to set the different color ranges for the cozmo to detect'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global ballColorEntries
        global trayColorEntries

        self.columnconfigure(0, pad=10, uniform=True, weight=1)
        self.columnconfigure(1, pad=3, uniform=True, weight=1)
        self.columnconfigure(2, pad=3, uniform=True, weight=1)
        self.columnconfigure(3, pad=3, uniform=True, weight=1)
        self.columnconfigure(4, pad=10, uniform=True, weight=1)

        self.rowconfigure(0, pad=3, uniform=True, weight=1)
        self.rowconfigure(1, pad=3, uniform=True, weight=1)
        self.rowconfigure(2, pad=3, uniform=True, weight=1)

        def setTextInput(textboxType,text):
            #textExample.delete(1.0,"end")
            if textboxType == "ball":
                ballColorText.insert(1.0, text)
            else:
                trayColorText.insert(1.0, text)
        def deleteTextInput(textboxType,line):
            if textboxType == "ball":
                ballColorText.insert(1.0, text)
            else:
                trayColorText.insert(1.0, text)
       

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        self.frame_1_0_video_feed = tk.Frame(self)
        self.canvas = tk.Canvas(self.frame_1_0_video_feed, width = 600, height = 450, bg="red")
        

        self.frame_1_0_video_feed.configure(bg="white",highlightbackground="black",highlightthickness=10)
        #colorLogLabelt = tk.Label(self.frame_1_0_video_feed, text="Color Log Log Log Log Log Log Log Log Log Log Log Log  Log Log Log Log Log  Log Log Log Log Log", pady=3, bg="red",wraplength=750, font=("Fixedsys", 50),justify="center").pack()
        self.canvas.pack()
        self.frame_1_0_video_feed.grid(row=0,column=1, rowspan=2,columnspan=4)
        
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_0_0 = tk.Frame(self)
        frame_0_0.configure(bg="white")

        colorLogLabel = tk.Label(frame_0_0, text="Color Log", pady=3, bg="white", font=("Fixedsys", 17), wraplength=100,justify="center").pack()
        ballColorsLabel = tk.Label(frame_0_0, text="Ball Colors:", pady=3, bg="white", font=controller.textFont, justify="left").pack()
        addBallColorBtn = tk.Button(frame_0_0, text="Add Ball Color", bg="white", font=controller.textFont,command=lambda:setTextInput("ball","new content \n")).pack()
        deleteBallColorBtn = tk.Button(frame_0_0, text="Delete Ball Color", bg="white",font=controller.textFont).pack()
        viewBallColorsBtn = tk.Button(frame_0_0, text="View Ball Colors", bg="white",font=controller.textFont).pack()

        ballColorText = tk.Text(frame_0_0,width=15, height=5,bg="gray")
        ballScrollbar = tk.Scrollbar(frame_0_0)
        ballScrollbar.config(command=ballColorText.yview)
        ballColorText.config(yscrollcommand=ballScrollbar.set)
        ballScrollbar.pack(side="right", fill=tk.Y)
        ballColorText.pack(side="left", fill="both", expand=True)

        frame_0_0.grid(row=0, column=0)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_0_1 = tk.Frame(self)
        frame_0_1.configure(bg="white")

        trayColorsLabel = tk.Label(frame_0_1, text="Tray Colors:", pady=3, bg="white", font=controller.textFont, justify="left").pack()
        addTrayColorBtn = tk.Button(frame_0_1, text="Add Tray Color", bg="white", font=controller.textFont, command=lambda:setTextInput("tray","new content \n")).pack()
        deleteTrayColorBtn = tk.Button(frame_0_1, text="Delete Tray Color", bg="white",font=controller.textFont).pack()
        viewTrayColorBtn = tk.Button(frame_0_1, text="View Tray Colors", bg="white",font=controller.textFont).pack()
        trayColorText = tk.Text(frame_0_1,width=15, height=5,bg="gray")
        trayScrollbar = tk.Scrollbar(frame_0_1)
        trayScrollbar.config(command=trayColorText.yview)
        trayColorText.config(yscrollcommand=trayScrollbar.set)
        trayScrollbar.pack(side="right", fill=tk.Y)
        trayColorText.pack(side="left", fill="both", expand=True)
        
        frame_0_1.grid(row=1, column=0)
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_4_0 = tk.Frame(self)
        frame_4_0.configure(bg="white")

        resumeButton = tk.Button(frame_4_0,text = "Resume Feed", bg="white", height=controller.buttonHeight, width=12,font=controller.textFont).pack()
        takeImageButton = tk.Button(frame_4_0,text = "Take Image", bg="white", height=controller.buttonHeight, width=12,font=controller.textFont).pack()

        frame_4_0.grid(row=0, column=4)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_1_2 = tk.Frame(self)
        frame_1_2.configure(bg="white")

        polygonButton = tk.Button(frame_1_2,text = u'\u2022', bg="white", height=0, width=10,font=controller.iconFont).pack()

        frame_1_2.grid(row=2, column=1)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_2_2 = tk.Frame(self)
        frame_2_2.configure(bg="white")

        rectangleButton = tk.Button(frame_2_2,text = u'\u25A1', bg="white", height=0, width=10,font=controller.iconFont).pack()

        frame_2_2.grid(row=2, column=2)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_3_2 = tk.Frame(self)
        frame_3_2.configure(bg="white")

        circleButton = tk.Button(frame_3_2,text = u'\u25EF', bg="white", height=0, width=10,font=controller.iconFont).pack()

        frame_3_2.grid(row=2, column=3)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_4_2 = tk.Frame(self)
        frame_4_2.configure(bg="white")

        eraserButton = tk.Button(frame_4_2,text = u'\u232B', bg="white", height=0, width=10,font=controller.iconFont).pack()

        frame_4_2.grid(row=2, column=4)
        
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        frame_0_2 = tk.Frame(self)
        frame_0_2.configure(bg="white")

        finishButton = tk.Button(frame_0_2, text="finish", pady=3, bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=int(controller.buttonWidth/3), command=lambda: controller.show_frame("FindingBallsPage"))
        finishButton.pack()
        backButton = tk.Button(frame_0_2, text="back", pady=3, bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=int(controller.buttonWidth/3), command=lambda: controller.show_frame("HomePage"))
        backButton.pack()

        frame_0_2.grid(row=2, column=0)
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def displayFeed(self,robot: cozmo.robot.Robot):
        while True:
            self.canvas.create_image(300,225,anchor="center",image=self.cozmoGetImage(robot))
            self.canvas.configure(bg="lightblue")
            self.canvas.pack()
            time.sleep(config.refreshTime) 

class FindingBallsPage(tk.Frame,CozmoReturnImage):
    '''This page is for the finding balls process'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.columnconfigure(0, pad=10, uniform=True, weight=1)
        self.columnconfigure(1, pad=3, uniform=True, weight=1)
        self.columnconfigure(2, pad=3, uniform=True, weight=1)
        self.columnconfigure(3, pad=3, uniform=True, weight=1)
        self.columnconfigure(4, pad=10, uniform=True, weight=1)

        self.rowconfigure(0, pad=3, uniform=True, weight=1)
        self.rowconfigure(1, pad=3, uniform=True, weight=1)
        self.rowconfigure(2, pad=3, uniform=True, weight=1)
        self.rowconfigure(3, pad=3, uniform=True, weight=1)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        titleFrame = tk.Frame(self)
        titleFrame.configure(bg="white")
        findingBallsLabel = tk.Label(titleFrame, text="Program Page",bg="white",font=controller.titleFont)
        findingBallsLabel.pack()
        titleFrame.grid(row=0, column=0, rowspan=1, columnspan=5)

        self.frame_1_0_video_feed = tk.Frame(self)
        self.canvas = tk.Canvas(self.frame_1_0_video_feed, width = 600, height = 450, bg="red")
        self.frame_1_0_video_feed.configure(bg="white",highlightbackground="black",highlightthickness=10)

        #colorLogLabelt = tk.Label(self.frame_1_0_video_feed, text="Color Log Log Log Log Log Log Log Log Log Log Log Log  Log Log Log Log Log  Log Log Log Log Log", pady=3, bg="red",wraplength=750, font=("Fixedsys", 50),justify="center").pack()
        self.canvas.pack()
        self.frame_1_0_video_feed.grid(row=1,column=0, rowspan=2,columnspan=5)

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        instruction_frame = tk.Frame(self)
        instruction_frame.grid(row=3, column=1, rowspan=1, columnspan=4)
        instruction_label = tk.Label(instruction_frame, text="Use the W,S,A,D keys to control the cozmo if it gets stuck in an area",bg="white",font=controller.textFont)
        instruction_label.pack()


        frame_0_2 = tk.Frame(self)
        frame_0_2.configure(bg="white")

        finishButton = tk.Button(frame_0_2, text="quit", pady=3, bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=int(controller.buttonWidth/3), command=lambda: controller.show_frame("ProgramTerminatedPage"))
        finishButton.pack()
        backButton = tk.Button(frame_0_2, text="back", pady=3, bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=int(controller.buttonWidth/3), command=lambda: controller.show_frame("SetColorsPage"))
        backButton.pack()

        frame_0_2.grid(row=3, column=0)
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def displayFeed(self,robot: cozmo.robot.Robot):
        while True:
            self.canvas.create_image(300,225,anchor="center",image=self.cozmoGetImage(robot))
            self.canvas.configure(bg="lightblue")
            self.canvas.pack()
            time.sleep(config.refreshTime) 

class ErrorPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        text = tk.Label(self, text="An error occured. Please restart the program", bg="white", font = controller.textFont)
        text.pack()

class ProgramTerminatedPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        text = tk.Label(self, text="PROGRAM TERMINATED", bg="white",font=controller.textFont)
        text.pack()
        space1 = tk.Label(self,bg="white")
        space1.pack()
        text2 = tk.Label(self,text="To rerun this application, please exit and restart.",bg="white",font=controller.textFont)
        text2.pack()

def cozmo_program(robot: cozmo.robot.Robot):
    cozmoObj = CozmoReturnImage(robot)
    setColorsThread = threading.Thread(target=gui.setColorsObj.displayFeed, args=[robot]) #start cozmo video feed for setcolorspage
    setColorsThread.start()
    gui.findBallsObj.displayFeed(robot) #start cozmo video feed for findingballspage

if __name__ == "__main__":
    gui = GUI()
    gui.wm_geometry("800x800+300+100")
    cozmoThread = threading.Thread(target=cozmo.run_program, args=[cozmo_program])
    cozmoThread.start()
    gui.mainloop()
