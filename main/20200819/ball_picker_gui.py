try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.titleFont = tkfont.Font(family='Fixedsys', size=50)
        self.subtitleFont = tkfont.Font(family='Fixedsys', size=20)
        self.buttonFont = tkfont.Font(family='Fixedsys', size=12)
        self.textFont = tkfont.Font(family='Fixedsys', size=12)
        self.buttonHeight = 2
        self.buttonWidth = 25

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, TutorialPage, AboutPage): #Namse of all the pages
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

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

        button1 = tk.Button(self, text="continue", bg="white", font=controller.buttonFont, height=controller.buttonHeight, width=controller.buttonWidth, command=lambda: controller.show_frame("PageOne"))
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


if __name__ == "__main__":
    gui = GUI()
    gui.wm_geometry("600x600+500+200")
    gui.mainloop()
