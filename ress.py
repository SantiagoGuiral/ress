"""
----------SANTIAGO RIOS GUIRAL--------------------------------------------------
----------santiago.riosg@udea.edu.co--------------------------------------------
--------------------------------------------------------------------------------
----------EMMANUEL GOMEZ OSPINA-------------------------------------------------
----------emmanuel.gomezo@udea.edu.co-------------------------------------------
--------------------------------------------------------------------------------
----------Curso Básico de Procesamiento de Imágenes y Visión Artificial---------
--------------------------------------------------------------------------------
"""


import tkinter as tk
from tkinter import messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

import detectChessBoard as dcb
import utils as utils
import motion as md
import diff as diff

url = "video/video25.mp4"

window = tk.Tk()
cap = cv2.VideoCapture(url)

board_recognized = False
start_detection = False
start_diff = False
borders = None
rect = None
frame_prevdiff = None
frame_actdiff = None
previous_frame = None
actual_frame = None
start_count = False
cnt_motion = 0
cnt_hand = 0
cnt_moves = 0
pos = utils.initial_position()
pgn = ""

def show_frame():
	global frame, rect, borders, boardw, boardh, pos, pgn, start_diff, frame_prevdiff, frame_actdiff, cnt_motion, cnt_hand, start_count, previous_frame, actual_frame, cnt_moves
	prev_frame = None
	# Establece si hay una cámara disponible
	if cap.isOpened():

		if prev_frame == None: 
			ret, prev_frame = cap.read() # Obtiene la imágen previa para comparar los fotogramas en la detección de movimiento
		else:
			prev_frame = frame

		# Captura de la toma desde la cámara
		ret, frame = cap.read() # Imágen actual

		# Detección del movimiento
		if start_detection == True:
			if start_diff == True:
				frame_prevdiff = frame
				start_diff = False

			motion = md.get_motion(prev_frame, frame) # Obtiene la variable booleana que indica si hay movimiento dentro del tablero de ajedrez
			if motion == False: # Si no hay movimiento ejecuta la sección del código que determina el registro de movimiento de las piezas
				cnt_hand += 1
				if cnt_hand >= 3: # Deja pasar 3 fotogramas para evitar interferencia de la mano del jugador
					cnt_hand = 0

					frame_prevdiff = dcb.get_perspective(borders, rect, boardw, boardh, frame_prevdiff) # Obtiene la perspectiva de la imágen previa
					frame_actdiff = dcb.get_perspective(borders, rect, boardw, boardh, frame) # Obtiene la perspectiva de la imágen actual
					movement = diff.check_difference(frame_prevdiff, frame_actdiff) # Compara las imágenes y determina si alguna ficha se movio
					#print (f'movement {movement}')
					if movement == True: # Si hubo movimiento guarda la imágen previa
						start_count = True
						previous_frame = frame_prevdiff

					if start_count == True:
						cnt_motion += 1

					if cnt_motion  >= 4: # Deja pasar 4 fotogramas para capturar la nueva imágen actual y evitar que la mano del jugador oculté las piezas
						start_count = False
						cnt_motion = 0
						cnt_moves += 1

						ret, actual_frame = cap.read() # Captura la imágen actual
						actual_frame = dcb.get_perspective(borders, rect, boardw, boardh, actual_frame) # Perspectiva de la imágen actual
						wc, hc = utils.rect_size(boardw, boardh) # Obtiene las dimensiones de las casillas del tablero
						coordinates = diff.difference(previous_frame, actual_frame) # Obtiene las coordenadas de los contornos obtenidos en la diferencia
						coordinate = utils.get_square(wc, hc, coordinates) #Obtiene la identificación de las casillas
						pos, piece, move = utils.get_piece_move(pos, coordinate, cnt_moves) # Registra el movimiento de las piezas
						print(f'piece: {piece} move: {move}')
						print(f'pos dict {pos}')
						pgn = utils.update_pgn(pgn, move) # Actualiza el historial de movimientos
					frame_prevdiff = frame
			#print(f'motion {motion}')

		prev_frame = frame
		# Muestra la captura de pantalla en la interfaz del programa
		frameshow = frame
		frameshow = cv2.resize(frameshow, (600, 400)) # Cambia el tamaño de la imágen para mostrarla en la interfaz
		img1 = cv2.cvtColor(frameshow, cv2.COLOR_BGR2RGBA) # Convierte al espacio RGB
		img2 = Image.fromarray(img1)
		img3 = ImageTk.PhotoImage(image = img2)
		framecap.img3 = img3
		framecap.configure(image = img3) # Muestra la captura de la cámara en la interfaz
		framecap.after(10, show_frame) # Ejecuta de nuevo esta función recursiva"
	
	
def recognize_board(cframe):
	""" Determina la presencia del tablero de ajedre y obtiene las coordenadas donde se van a realizar las 
	operación y técnicas de procesamiento de imágenes. Retorna las coordenadas de los vertices del tablero.
	"""
	global board, rect, borders, boardw, boardh, board_recognized
	board_recognized = True
	capture_frame = cframe.copy()
	image1 = dcb.get_chessboardborders(capture_frame) # Obtiene la imágen con los bordes de la captura usando Canny
	contour = dcb.get_chessboardcontour(image1) # Obtiene el contorno de mayor tamaño correspondiente al tablero de ajedrez
	rect, boardw, boardh = dcb.get_chessboardrect(contour) # Obtiene el tamaño idal del tablero para obtener su perspectiva vertical
	contours, image2 = dcb.get_chessboardhull(image1, contour) # Obtiene el contorno del polígono que forma el tablero y su imágen
	borders = dcb.get_chessboardcoordinates(image2, contours) # Obtiene las coordenadas de los vertices del tablero

	# Establece si hay presencia del tablero de ajedrez en la captura
	if borders == None:
		state_label.configure(text = "State: Not Succesful", bg = 'white', fg = 'red', font = 'bold')
	else:
		if (len(borders) == 4 and len(rect) == 4):
			board = dcb.get_perspective(borders, rect, boardw, boardh, cframe) # Obtiene la perspectiva vertical del tablero de ajedrez
			state_label.configure(text = "State: Succesful", bg = 'white', fg = 'green', font = 'bold')
			print(f'borders cv2: {borders}')
			print(f'rectangle: {rect}')

		else:
			state_label.configure(text = "State: Not Succesful", bg = 'white', fg = 'red', font = 'bold')


def start():
	"""Indica el inicio de la captura de los movimientos de las piezas en el tablero de ajedrez.
	"""
	global start_detection, start_diff
	start_diff = True # Variable booleana que indica que se puede iniciar a comparar las imágenes
	start_detection = True # Variable que inidica el inicio de la detección de movimiento

	recording_label.configure(text = 'Recording State: On', bg = 'white', fg = 'green', font = 'bold')


def finish():
	"""Finalizá el registro de movimientos en la partida de ajedrez. También permite generar el archivo de texto con el
	historial de la partida y generá el archivo PGN.
	"""
	global start_detection
	start_detection = False # Variable booleana que para el registro de los movimientos
	utils.save_pgn(pgn) # Guarda el historial de la partida y genera el archivo de texto para el formato PGN

	pgn_label.configure(text = "PGN State: Saved successfully", bg = 'white', fg = 'green', font = 'bold')
	recording_label.configure(text = 'Recording State: Off', bg = 'white', fg = 'red', font = 'bold')
	cap.release()	# Suelta el control del programa sobre la cámara del computador
	cv2.destroyAllWindows()


def help_view():
	""" Ventana desplegable con la ayuda para manejar el programa.
	"""
	filewin = tk.Toplevel()
	filewin.title("Help")
	with open("./resources/help.txt",'r') as f:
		about_text = f.read()
		l = tk.Label(filewin, text = about_text, justify = "left").pack(padx = 8, pady = 8, fill = 'both', expand = True)


def help_about():
	"""Ventana desplegable con información de interes.
	"""
	filewin = tk.Toplevel()
	filewin.title("About")
	with open("./resources/about.txt",'r') as f:
		about_text = f.read()
		l = tk.Label(filewin, text = about_text, justify = "center").pack(padx = 8,pady = 8, fill = 'both', expand = True)


def close_all():
	"""Cierra la cáamra y la libera.
	"""
	cap.release()	# Suelta el control del programa sobre la cámara del computador
	cv2.destroyAllWindows()


# ------------------------------------------------------------------------------
# Configuración de la interfaz y asociados -------------------------------------
# ------------------------------------------------------------------------------

# Menu superior
menubar = tk.Menu(window)

# Submenu para cerrar la cámara y el programa
menufile = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = menufile)
menufile.add_command(label = "Close Capture", command = close_all)
menufile.add_command(label = "Exit", command = window.quit)

# Submenu con la ayuda para manipular el programa
helpmenu = tk.Menu(menubar, tearoff = 0)
helpmenu.add_command(label = "Help", command = help_view)
helpmenu.add_command(label = "About", command = help_about)
menubar.add_cascade(label = "Help", menu = helpmenu)

window.config(menu = menubar)
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file = './resources/icon.png'))

w = 1200 # Ancho de la interfaz
h = 800 # Alto de la interfaz
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry('%dx%d+%d+%d' % (w, h, x, y)) # Centra la interfaz en la pantalla
window.title("Chess Register Moves: Ress")


# ------------------------------------------------------------------------------
# Ventana principal del programa -----------------------------------------------
# ------------------------------------------------------------------------------

main = tk.Frame(window)
main.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
main.configure(bg = 'white')

# ---------------------- Sección: Título del programa -------------------------#

title_label = tk.Label(main, text = "Register of Chess Movements")
title_label.place(relx = 0.5, rely = 0.05, anchor = 'center')
title_label.configure(bg = 'white', fg = 'black', font = ("Arial", 25))

# ---------------------- Sección: Captura de video ----------------------------#

# Sección para mostrar la captura desde la cámara
video = tk.LabelFrame(main, text = 'Game', font = 'hold')
video.place(relx = 0.01, rely = 0.1, relwidth = 0.58, relheight = 0.85)
video.configure(bg = 'white')

# Ventana con la captura de video
framecap = tk.Label(video)
framecap.grid(row = 0, column = 0, padx = 24, pady = 100)

# --------------------- Sección: Control del programa -------------------------#

control = tk.LabelFrame(main, text = 'Control', font = 'bold')
control.place(relx = 0.61, rely = 0.1, relwidth = 0.38, relheight = 0.85)
control.configure(bg = 'white')

# --------------------- Sección: Reconocimiento del tablero -------------------#

# Botón que captura la imágen para obtener las coordenadas del tablero
recognize_frame = tk.LabelFrame(control, text = "Recognition of the Chessboard", font = 'bold')
recognize_frame.place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.35)
recognize_frame.configure(bg = 'white')

# Botón que reconoce el tamaño y determina sus dimensiones y coordenadas
rec_btn = tk.Button(recognize_frame, text = 'Recognize Board', bg ='#5d5e43', font = ' bold', fg = 'white', command = lambda:recognize_board(frame))
rec_btn.place(relx = 0.1, rely = 0.25, relwidth = 0.8, relheight = 0.3)

# Texto que indica el estado del reconocimiento inicial del tablero
state_label = tk.Label(recognize_frame, text = "State: ")
state_label.place(relx = 0.1, rely = 0.65)
state_label.configure(bg = 'white', fg = 'red', font = 'bold')

# --------------------- Sección: Control de la partida ------------------------#

game_frame = tk.LabelFrame(control, text = "Chess Game Capture", font = 'bold')
game_frame.place(relx = 0.05, rely = 0.45, relwidth = 0.9, relheight = 0.5)
game_frame.configure(bg = 'white')

# Texto que indica el estado de grabación de la partida
recording_label = tk.Label(game_frame, text = "Recording State: Off ")
recording_label.place(relx = 0.1, rely = 0.1)
recording_label.configure(bg = 'white', fg = 'red', font = 'bold')

# Botón que inicia la captura de la partida de ajedrez
cap_btn = tk.Button(game_frame, text = 'Start Recording', bg = '#5d5e43', font = 'bold', fg = 'white', command = start)
cap_btn.place(relx = 0.1, rely = 0.25, relwidth = 0.8, relheight = 0.2)

# Botón que finaliza la captura de la partida de ajedrez y genera un archivo txt con los movimientos en formato PGN
fin_btn = tk.Button(game_frame, text = 'Stop Recording', bg = '#5d5e43', font = 'bold', fg = 'white', command = finish)
fin_btn.place(relx = 0.1, rely = 0.55, relwidth = 0.8, relheight = 0.2)

# Texto que indica el estado final del programa
pgn_label = tk.Label(game_frame, text = "PNG State: Not saved")
pgn_label.place(relx = 0.1, rely =0.8)
pgn_label.configure(bg = 'white', fg = 'red', font = 'bold')

show_frame()
window.mainloop()
cap.release()	# Suelta el control del programa sobre la cámara del computador
