'''again, unfinished, just an outline'''
import tkinter as tk
from tkinter.font import Font

window = tk.Tk()
window.configure(bg="white")
window.geometry("400x300")
'''Setting Font Types'''
titleFont = Font(family="Fixedsys",size=50)
subtitleFont = Font(family="Fixedsys",size=20)
buttonFont = Font(family="Fixedsys",size=15)

'''home button functions'''
def btnHomeContinue():
    print("continue")

def btnHomeTutorial():
    print("tutorial")

def btnHomeAbout():
    print("about")

'''Home Page title and subtitle'''
titleText = "COZMO"
subtitleText = "Ball Picker"
lbl_home_title = tk.Label(text=titleText,font=titleFont,fg="blue",bg="white")
lbl_home_subtitle = tk.Label(text=subtitleText,font=subtitleFont,bg="white")

'''Home Page Buttons'''
home_button_width = 25
home_button_height = 2
btn_home_continue = tk.Button(text="continue",font=buttonFont,width=home_button_width,height=home_button_height,command=btnHomeContinue)
btn_home_tutorial = tk.Button(text="tutorial",font=buttonFont,width=home_button_width,height=home_button_height,command=btnHomeTutorial)
btn_home_about = tk.Button(text="about",font=buttonFont,width=home_button_width,height=home_button_height,command=btnHomeAbout)


#lbl_test.configure()
lbl_home_title.pack()
lbl_home_subtitle.pack()
btn_home_continue.pack()
btn_home_tutorial.pack()
btn_home_about.pack()
window.mainloop()
