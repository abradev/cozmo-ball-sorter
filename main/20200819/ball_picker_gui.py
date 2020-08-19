import tkinter as tk

'''unfinished gui, just a frame for how to switch pages'''

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class HomePage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the homepage")
       label.pack(side="top", fill="both", expand=True)

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
       label = tk.Label(self, text="This is the tutorial page")
       label.pack(side="top", fill="both", expand=True)

class AboutPage(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the about page")
       label.pack(side="top", fill="both", expand=True)

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

        home_page.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
