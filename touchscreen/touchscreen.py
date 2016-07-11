#!/usr/bin/env python2
from Tkinter import *

root = Tk()

def Correct():
    print ("reward")

def Incorrect():
    print ("timeout")

circle=PhotoImage(file='circle.png')

frame1=Frame(root)
frame1.pack(side=TOP, fill=X)
star=PhotoImage(file='star.png')
button1=Button(frame1, compound=TOP, width=683, height=768, image=star, command=Correct)
button1.pack(side=LEFT, padx=2, pady=2)

button2=Button(frame1, compound=TOP, width=683, height=768, image=circle, command=Incorrect)
button2.pack(side=RIGHT, padx=2, pady=2)

root.geometry('{}x{}'.format(1366,768))

root.mainloop()
root.destroy()
