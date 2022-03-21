import tkinter as tk
from tkinter import messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

import detectChessBoard as dcb

global coordinates

url = 0 # "https://192.168.0.15:8080/video"

window = tk.Tk()
cap = cv2.VideoCapture(url)

def show_frame():
	global frame
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	img2 = Image.fromarray(img1)
	img3 = ImageTk.PhotoImage(image = img2)
	framecap.img3 = img3
	framecap.configure(image=img3)
	framecap.after(10, show_frame)
	
def recognize_board(frame):
	
	plt.imshow(frame)
	plt.savefig("frame.png")
	state_label.configure(text = "State: Succesful")

def finish():
	pass

def start():
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


# ------------------------------------------------------------------------------
# Configuración de la interfaz y asociados -------------------------------------
# ------------------------------------------------------------------------------

menubar = tk.Menu(window)

menufile = tk.Menu(menubar, tearoff = 0)
menufile.add_command(label = "Exit", command = window.quit)
menubar.add_cascade(label = "File", menu = menufile)

helpmenu = tk.Menu(menubar, tearoff = 0)
helpmenu.add_command(label = "Help", command = help_view)
helpmenu.add_command(label = "About", command = help_about)
menubar.add_cascade(label = "Help", menu = helpmenu)

window.config(menu = menubar)
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file = './resources/icon.png'))

w = 1200
h = 800
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
window.title("Chess Register Moves: Ress")

#
#
#


# ------------------------------------------------------------------------------
# Ventana principal del programa -----------------------------------------------
# ------------------------------------------------------------------------------

main = tk.Frame(window)
main.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
main.configure(bg = 'white')

# ---------------------- Sección: Captura de video ----------------------------#

video = tk.LabelFrame(main, text = 'Game', font = 'hold')
video.place(relx = 0.01, rely = 0.05, relwidth = 0.58, relheight = 0.9)
video.configure(bg = 'white')

# Ventana con la captura de video
framecap = tk.Label(video)
framecap.grid(row = 0, column = 0, padx = 24, pady = 100)

# --------------------- Sección: Control del programa -------------------------#

control = tk.LabelFrame(main, text = 'Control', font = 'bold')
control.place(relx = 0.61, rely = 0.05, relwidth = 0.38, relheight = 0.9)
control.configure(bg = 'white')

# --------------------- Sección: Reconocimiento del tablero -------------------#

recognize_frame = tk.LabelFrame(control, text = "Reconocimiento del tablero", font = 'bold')
recognize_frame.place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.35)
recognize_frame.configure(bg = 'white')

# Botón que reconoce el tamaño y determina sus dimensiones y coordenadas
rec_btn = tk.Button(recognize_frame, text = 'Recognize Board', bg ='#5d5e43', font = ' bold', fg = 'white', command = lambda:recognize_board(frame))
rec_btn.place(relx = 0.1, rely =0.25, relwidth = 0.8, relheight = 0.3)

# Texto que indica el estado del reconocimiento inicial del tablero
state_label = tk.Label(recognize_frame, text = "State: ")
state_label.place(relx = 0.1, rely =0.65)
state_label.configure(bg = 'white', fg = 'red', font = 'bold')

# --------------------- Sección: Control de la partida ------------------------#

game_frame = tk.LabelFrame(control, text = "Captura de la partida", font = 'bold')
game_frame.place(relx = 0.05, rely = 0.45, relwidth = 0.9, relheight = 0.5)
game_frame.configure(bg = 'white')

# Botón que inicia la captura de la partida de ajedrez
cap_btn = tk.Button(game_frame, text = 'Start Recording', bg = '#5d5e43', font = 'bold', fg = 'white', command=start)
cap_btn.place(relx = 0.1, rely = 0.15, relwidth = 0.8, relheight = 0.2)

# Botón que finaliza la captura de la partida de ajedrez y genera un archivo txt con los movimientos en formato PGN
fin_btn = tk.Button(game_frame, text = 'Stop Recording', bg = '#5d5e43', font = 'bold', fg = 'white', command=finish)
fin_btn.place(relx = 0.1, rely = 0.5, relwidth = 0.8, relheight = 0.2)

# Texto que indica el estado final del programa
png_label = tk.Label(game_frame, text = "PNG State: ")
png_label.place(relx = 0.1, rely =0.8)
png_label.configure(bg = 'white', fg = 'red', font = 'bold')

show_frame()
window.mainloop()
