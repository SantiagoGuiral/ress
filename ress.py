import tkinter as tk
import cv2
import numpy as np


window = tk.Tk()

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
video.place(relx = 0.01, rely = 0.05, relwidth = 0.48, relheight = 0.9)
video.configure(bg = 'white')

# control frame
control = tk.LabelFrame(main, text = 'Control', font = 'bold')
control.place(relx = 0.51, rely = 0.05, relwidth = 0.48, relheight = 0.9)
control.configure(bg = 'white')

window.mainloop()
