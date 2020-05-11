from tkinter import *

""" Test for full screen window form"""

"""
my_window = Tk()

my_window.geometry("%dx%d+0+0" % (my_window.winfo_screenmmwidth(), my_window.winfo_screenmmheight()))
my_window.mainloop()
"""

my_window = Tk()

w = Label(my_window, text=" ")
my_window.overrideredirect(True)
my_window.geometry("{0}x{1}+0+0".format(my_window.winfo_screenwidth(), my_window.winfo_screenheight()))
my_window.focus_set()  # <-- move focus to this widget
my_window.bind("<Escape>", lambda e: e.widget.quit())
w.pack()

my_window.mainloop()
