import tkinter as tk
from tkinter import messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

import detectChessBoard as dcb

url = 0# "http://192.168.0.15:8080/video"

window = tk.Tk()
cap = cv2.VideoCapture(url)

def show_frame():
	global frame
	if cap.isOpened():
		ret, frame = cap.read()
		frameshow = frame.copy()
		frameshow = cv2.resize(frameshow, (600, 400))
		img1 = cv2.cvtColor(frameshow, cv2.COLOR_BGR2RGBA)
		img2 = Image.fromarray(img1)
		img3 = ImageTk.PhotoImage(image = img2)
		framecap.img3 = img3
		framecap.configure(image=img3)
		framecap.after(10, show_frame)
	
def recognize_board(cframe):
	global board, rect, borders
	capture_frame = cframe.copy()
	image1 = dcb.get_chessboardborders(capture_frame)
	contour = dcb.get_chessboardcontour(image1)
	rect, w, h = dcb.get_chessboardrect(contour)
	contours, image2 = dcb.get_chessboardhull(image1, contour)
	borders = dcb.get_chessboardcoordinates(image2, contours)

	if borders == None:
		state_label.configure(text = "State: Not Succesful")
	else:
		if (len(borders) == 4 and len(rect) == 4):
			board = dcb.get_perspective(borders, rect, w, h, cframe)
			state_label.configure(text = "State: Succesful")

			plt.imshow(board)
			plt.savefig('board.png')
			print(f'borders cv2: {borders}')
			print(f'rect {rect}')

		else:
			state_label.configure(text = "State: Not Succesful")

def start():
	pass


def finish():
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

def close_all():
	cap.release()	# Suelta el control del programa sobre la cámara del computador
	cv2.destroyAllWindows()

# ------------------------------------------------------------------------------
# Configuración de la interfaz y asociados -------------------------------------
# ------------------------------------------------------------------------------

menubar = tk.Menu(window)

menufile = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = menufile)
menufile.add_command(label = "Close cam", command = close_all)
menufile.add_command(label = "Exit", command = window.quit)

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
cap.release()	# Suelta el control del programa sobre la cámara del computador
