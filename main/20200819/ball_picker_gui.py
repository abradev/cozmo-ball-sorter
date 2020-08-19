import tkinter as tk
from tkinter.font import Font

'''unfinished'''

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class HomePage(Page):
    def __init__(self,*args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        titleFont = Font(family="Fixedsys",size=50)
        subtitleFont = Font(family="Fixedsys",size=20)
        buttonFont = Font(family="Fixedsys",size=15)

        '''Home Page title and subtitle'''
        titleText = "COZMO"
        subtitleText = "Ball Picker"
        lbl_home_title = tk.Label(self,text=titleText,font=titleFont,fg="blue",bg="white")
        lbl_home_subtitle = tk.Label(self,text=subtitleText,font=subtitleFont,bg="white")
        space1 = tk.Label(self,bg="white")
        '''Home Page Buttons'''
        home_button_width = 25
        home_button_height = 2
        btn_home_continue = tk.Button(self,text="continue",font=buttonFont,width=home_button_width,height=home_button_height)
        btn_home_tutorial = tk.Button(self,text="tutorial",font=buttonFont,width=home_button_width,height=home_button_height)
        btn_home_about = tk.Button(self,text="about",font=buttonFont,width=home_button_width,height=home_button_height)

        '''packing elements'''
        lbl_home_title.pack()
        lbl_home_subtitle.pack()
        space1.pack()
        btn_home_continue.pack()
        btn_home_tutorial.pack()
        btn_home_about.pack()

class NumColorsPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is numcolorspage")
       label.pack(side="top", fill="both", expand=True)

class SetColorsPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is setcolorspage")
       label.pack(side="top", fill="both", expand=True)

class ColorsLogPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is colorslogpage")
       label.pack(side="top", fill="both", expand=True)

class FindingBallsPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the finding balls page")
       label.pack(side="top", fill="both", expand=True)

class TutorialPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        buttonFont = Font(family="Fixedsys",size=15)

        space1 = tk.Label(self,bg="white")
        tutorial_text = tk.Label(self,text="Video for program will go here",wraplength=300,justify="center",bg="white")
        space2 = tk.Label(self,bg="white")
        button_width = 25
        button_height = 2
        btn_back = tk.Button(self,text="back",font=buttonFont,width=button_width,height=button_height)
    
        space1.pack()
        tutorial_text.pack()
        space2.pack()
        btn_back.pack()

class AboutPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        buttonFont = Font(family="Fixedsys",size=15)

        space1 = tk.Label(self,bg="white")
        aboutBullet1 = tk.Label(self, text="•The Cozmo Ball Sorter is a project that enables the Anki Cozmo to be placed in an environment of different colored balls and systematically deposit them in designated areas",wraplength=300,justify="left",bg="white")
        aboutBullet2 = tk.Label(self, text="•Using OpenCV to process images from the Cozmo, the program detects the balls and returns a coordinate to make the robot turn towards the ball",wraplength=300,justify="left",bg="white")
        aboutBullet3 = tk.Label(self, text="•This project was started in May 2020",wraplength=300,justify="left",bg="white")
        space2 = tk.Label(self,bg="white")
        link = tk.Label(self,text="Visit our Github repository to see the code for this project: [add link here] ",bg="white",wraplength=300)
        space3 = tk.Label(self,bg="white")
        button_width = 25
        button_height = 2
        btn_back = tk.Button(self,text="back",font=buttonFont,width=button_width,height=button_height)

        space1.pack()
        aboutBullet1.pack()
        aboutBullet2.pack()
        aboutBullet3.pack()
        space2.pack()
        link.pack()
        space3.pack()
        btn_back.pack()


class ProgramTerminatedPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is programterminatedpage")
       label.pack(side="top", fill="both", expand=True)

class ErrorPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is errorpage")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        home_page = HomePage(self)
        num_colors_page = NumColorsPage(self)
        set_colors_page = SetColorsPage(self)
        colors_log_page = ColorsLogPage(self)
        finding_balls_page = FindingBallsPage(self)
        tutorial_page = TutorialPage(self)
        about_page = AboutPage(self)
        program_terminated_page = ProgramTerminatedPage(self)
        error_page = ErrorPage(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        home_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        num_colors_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        set_colors_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        colors_log_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        finding_balls_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        tutorial_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        about_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        program_terminated_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        error_page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Home", command=home_page.lift)
        b2 = tk.Button(buttonframe, text="Num Colors", command=num_colors_page.lift)
        b3 = tk.Button(buttonframe, text="Set Colors", command=set_colors_page.lift)
        b4 = tk.Button(buttonframe, text="Colors Log", command=colors_log_page.lift)
        b5 = tk.Button(buttonframe, text="Finding Balls", command=finding_balls_page.lift)
        b6 = tk.Button(buttonframe, text="Tutorial", command=tutorial_page.lift)
        b7 = tk.Button(buttonframe, text="About", command=about_page.lift)
        b8 = tk.Button(buttonframe, text="Terminated", command=program_terminated_page.lift)
        b9 = tk.Button(buttonframe, text="Error", command=error_page.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")
        b6.pack(side="left")
        b7.pack(side="left")
        b8.pack(side="left")
        b9.pack(side="left")
        

        home_page.configure(bg="white")
        num_colors_page.configure(bg="white")
        set_colors_page.configure(bg="white")
        colors_log_page.configure(bg="white")
        finding_balls_page.configure(bg="white")
        tutorial_page.configure(bg="white")
        about_page.configure(bg="white")
        program_terminated_page.configure(bg="white")
        error_page.configure(bg="white")

        home_page.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("600x600")
    root.mainloop()
