import tkinter as tk
from tkinter import messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk

window = tk.Tk()

cap = cv2.VideoCapture(0)

def show_frame():
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	img2 = Image.fromarray(img1)
	img3 = ImageTk.PhotoImage(image = img2)
	framecap.img3 = img3
	framecap.configure(image=img3)
	framecap.after(10, show_frame)
	
def finish():
	pass

def recognize_board():
	pass

def help_view():
    filewin = tk.Toplevel()
    filewin.title("Help")
    with open("./resources/help.txt",'r') as f:
        about_text = f.read()
        l = tk.Label(filewin, text = about_text, justify = "left").pack(padx = 8, pady = 8, fill = 'both', expand = True)

def help_about():
    filewin = tk.Toplevel()
    filewin.title("About")
    with open("./resources/about.txt",'r') as f:
        about_text = f.read()
        l = tk.Label(filewin, text = about_text,justify = "center").pack(padx = 8,pady = 8, fill = 'both', expand = True)

# Menu
menubar = tk.Menu(window)

menufile = tk.Menu(menubar, tearoff = 0)
menufile.add_command(label = "Exit", command = window.quit)
menubar.add_cascade(label = "File", menu = menufile)

helpmenu = tk.Menu(menubar, tearoff = 0)
helpmenu.add_command(label = "Help", command = help_view)
helpmenu.add_command(label = "About", command = help_about)
menubar.add_cascade(label = "Help", menu = helpmenu)

window.config(menu = menubar)


w = 1200
h = 800
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.title("Chess Register Moves: Ress")

# main frame
main = tk.Frame(window)
main.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
main.configure(bg = 'white')

# show_video frame
video = tk.LabelFrame(main, text = 'Game', font = 'hold')
video.place(relx = 0.01, rely = 0.05, relwidth = 0.58, relheight = 0.9)
video.configure(bg = 'white')

# Capture image frame
framecap = tk.Label(video)
#framecap.place(relx = 0.05, rely = 0.20, relwidth = 0.90, relheight = 0.6)
framecap.grid(row = 0, column = 0, padx = 24, pady = 100)

# control frame
control = tk.LabelFrame(main, text = 'Control', font = 'bold')
control.place(relx = 0.61, rely = 0.05, relwidth = 0.38, relheight = 0.9)
control.configure(bg = 'white')

# recognize chessboard
rec_bt = tk.Button(control, text = 'Recognize Board', bg ='#5d5e43', font = ' bold', fg = 'white', command = recognize_board
)
rec_bt.place(relx = 0.2, rely =0.2, relwidth = 0.6, relheight = 0.1)

# init button
cap_bt = tk.Button(control, text = 'Start Recording', bg = '#5d5e43', font = 'bold', fg = 'white', command=show_frame)
cap_bt.place(relx = 0.2, rely = 0.4, relwidth = 0.6, relheight = 0.1)

# finish button
fin_capbt = tk.Button(control, text = 'Stop Recording', bg = '#5d5e43', font = 'bold', fg = 'white', command=finish)
fin_capbt.place(relx = 0.2, rely = 0.6, relwidth = 0.6, relheight = 0.1)


window.mainloop()
