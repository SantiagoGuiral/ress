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

import cv2
import numpy as np

def get_motion(prev_frame, frame):
	"""Determina cuando hay movimiento en el video que se está capturando en la partida de ajedrez.
	Recibe dos capturas de la imágen para compararlas (diferencia) y determinar si hay movimiento en el caso de que los
	jugadores estén moviendo las piezas en el tablero. La salida es un variable booleana que informa el estado de movimiento.
	"""
	kernel = np.ones((3, 3), np.uint8) # Elemento estructurante
	motion = False # Variable booleana que especifica el estado de movimiento
	
	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) # Convierte a escala de grises la imágen del estado anterior
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convierte a escala de grises la imágen del estado actual

	prev_blur = cv2.GaussianBlur(prev_gray, (5, 5), 1) # Suaviza la imágen del estado anterior
	blur = cv2.GaussianBlur(gray, (5, 5), 1) # Suaviza la imágen del estado anterior

	diff = cv2.absdiff(prev_blur, blur) # Obtiene la diferencia de las dos imágenes
	h, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY) # Binarización de la diferencia.
	dilated = cv2.dilate(thresh, kernel, iterations = 1) # Se dilatan los contornos obtenidos a tráves de la diferencia
	contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Se buscan los contornos presentes en la imágen
	
	# Si hay un contorno con área superior a 30 se determina que hubo movimiento en la imágen
	# Esto se debe a que hay una diferencia considerable entre las dos imágenes
	for contour in contours:
		if cv2.contourArea(contour) > 30: 
			motion = True
			break

	return motion
