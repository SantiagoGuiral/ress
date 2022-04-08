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
import matplotlib.pyplot as plt

def difference(prev_frame, frame):
	"""Compara las dos imágenes de entrada con la posición previa y la posición actual del movimiento de las piezas de ajedrez.
	Retorna las coordenadas de los centroides donde se detectó una diferencia entre las dos imágenes.
	Estos centros representan la posición de donde partió la ficha y la posición a donde llega esta.
	"""
	coordinates = [] # Lista con las coordenadas de los centroides
	kernel = np.ones((5, 5), np.uint8) # Elemento estructurante para la morfológia

	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) # Converite a escala de grises la imágen previa
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converite a escala de grises la imágen actual

	prev_blur = cv2.blur(prev_gray, (29, 29), 1) # Suaviza la imágen previa
	blur = cv2.blur(gray, (29, 29), 1)	# Suaviza la imágen posterior

	diff = cv2.absdiff(prev_blur, blur) # Obtiene la diferencia entre las dos imagenes
	diff = cv2.dilate(diff, kernel, iterations = 1) # Dilata los contornos donde se detecto diferencia

	h, thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY) # Binarización de los contornos

	# Apertura binaria para eliminar contornos muy pequeños que pueden causar error
	thresh = cv2.erode(thresh, kernel, iterations = 3) # Eroción
	thresh = cv2.dilate(thresh, kernel, iterations = 3) # Dilatación

	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Obtiene todos los contornos de la imágen
	list_contours = list(contours) # Convierte a una lista los contornos obtenidos


	# Obtiene las coordenadas de los centroides de los contornos
	if len(list_contours) == 2 or len(list_contours) == 3: # Mueve una sola pieza
		cnt1 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el primer contorno
		# Elimina el contorno para no duplicar las coordenadas del movimiento
		for i in range(len(list_contours)):
			try:
				if (cnt1 == list_contours[i]).all():
					break
			except:
				if (cnt1 == list_contours[i]):
					break	
		del list_contours[i]

		cnt2 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el segundo contorno de interes en el movimiento
	
		M1 = cv2.moments(cnt1) # Momentos del primer contorno
		x1 = int(M1["m10"]/M1["m00"]) # Posición en el eje x
		y1 = int(M1["m01"]/M1["m00"]) # Posición en el eje y
		c1 = (x1, y1) # Coordenadas del primer contorno

		M2 = cv2.moments(cnt2) # Momentos del segundo contorno
		x2 = int(M2["m10"]/M2["m00"]) # Posición en el eje x
		y2 = int(M2["m01"]/M2["m00"]) # Posición en el eje y
		c2 = (x2, y2) # Coordenadas del segundo contorno

		coordinates.append(c1) # Coordenadas del primer contorno
		coordinates.append(c2) # Coordenadas del segundo contorno
	elif len(list_contours) >= 4: # Movimiento conocido como castle
		cnt1 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el primer contorno
		for i in range(len(list_contours)):
			try:
				if (cnt1 == list_contours[i]).all():
					break
			except:
				if (cnt1 == list_contours[i]):
					break
		del list_contours[i]

		cnt2 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el segundo contorno
		for i in range(len(list_contours)):
			try:
				if (cnt2 == list_contours[i]).all():
					break
			except:
				if (cnt2 == list_contours[i]):
					break
		del list_contours[i]

		cnt3 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el tercer contorno
		for i in range(len(list_contours)):
			try:
				if (cnt3 == list_contours[i]).all():
					break
				except:
					if (cnt3 == list_contours[i]):
					break
		del list_contours[i]
	
		cnt4 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el cuarto contorno

		M1 = cv2.moments(cnt1) # Momentos del primer contorno
		x1 = int(M1["m10"]/M1["m00"]) # Posición en el eje x
		y1 = int(M1["m01"]/M1["m00"]) # Posición en el eje y
		c1 = (x1, y1) # Coordenadas del primer contorno

		M2 = cv2.moments(cnt2) # Momentos del segundo contorno
		x2 = int(M2["m10"]/M2["m00"]) # Posición en el eje x
		y2 = int(M2["m01"]/M2["m00"]) # Posición en el eje y
		c2 = (x2, y2) # Coordenadas del segundo contorno

		M3 = cv2.moments(cnt3) # Momentos del tercer contorno
		x3 = int(M3["m10"]/M3["m00"]) # Posición en el eje x
		y3 = int(M3["m01"]/M3["m00"]) # Posición en el eje y
		c3 = (x3, y3) # Coordenadas del tercer contorno

		M4 = cv2.moments(cnt4) # Momentos del cuarto contorno
		x4 = int(M4["m10"]/M4["m00"]) # Posición en el eje x
		y4 = int(M4["m01"]/M4["m00"]) # Posición en el eje y
		c4 = (x4, y4) # Coordenadas del cuarto contorno

		coordinates.append(c1)
		coordinates.append(c2)
		coordinates.append(c3)
		coordinates.append(c4)
	elif len(list_contours) == 3: # Movimiento de captura al pazo
		cnt1 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el primer contorno
		list_contours.remove(cnt1)
	
		cnt2 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el segundo contorno
		list_contours.remove(cnt2)

		cnt3 = max(list_contours, key = lambda x: cv2.contourArea(x)) # Obtiene el tercer contorno

		M1 = cv2.moments(cnt1) # Momentos del primer contorno
		x1 = int(M1["m10"]/M1["m00"]) # Posición en el eje x
		y1 = int(M1["m01"]/M1["m00"]) # Posición en el eje y
		c1 = (x1, y1) # Coordenadas del primer contorno

		M2 = cv2.moments(cnt2) # Momentos del segundo  contorno
		x2 = int(M2["m10"]/M2["m00"]) # Posición en el eje x
		y2 = int(M2["m01"]/M2["m00"]) # Posición en el eje y
		c2 = (x2, y2) # Coordenadas del segundo contorno

		M3 = cv2.moments(cnt3) # Momentos del tercer contorno
		x3 = int(M3["m10"]/M3["m00"]) # Posición en el eje x
		y3 = int(M3["m01"]/M3["m00"]) # Posición en el eje y
		c3 = (x3, y3) # Coordenadas del tercer contorno

		coordinates.append(c1)
		coordinates.append(c2)
		coordinates.append(c3)
	
	else:
		coordinates.append((0, 0))

	# Retorna las coordenadas de las contornos obtenidos de la diferncia entre las dos imágenes
	return coordinates


def check_difference(prev_frame, frame):
	"""Indica si hubo algún movimiento de las piezas de ajedrez. Para esto compara una imagen del tablero que se guardó antes de la
	detección de movimiento e indica si hay diferencia con la imágen actual guardada después de que se paró el movimiento.
	La función retorna una variable booleana que indica que una pieza en el tablero cambia de ubicación.
	"""
	movement = False # Variable que indica si alguna pieza cambio de ubicación

	kernel = np.ones((7, 7), np.uint8) # Elemento estructurante para la morfológia
	
	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) # Convierte a escala de grises la imágen previa
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convierte a escala de grises la imágen actual

	prev_blur = cv2.blur(prev_gray, (29, 29), 1) # Filtro para eliminar el ruido
	blur = cv2.blur(gray, (29, 29), 1) # Filtro para eliminar el ruido

	diff = cv2.absdiff(prev_blur, blur) # Obtiene la direncia entre las dos imágenes
	diff = cv2.dilate(diff, kernel, iterations = 2) # Dilata los contornos de la diferencia

	h, thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY) # Umbraliza los contornos
 	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Obtiene los contornos que hay en la imágen

	# Si hay contornos, se puede determinar que hubo un cambio en la posición de las piezas de ajedrez.
	if len(contours) != 0: 
		movement = True

	return movement


def detect_hand(frame):
	"""Determina si la mano del jugador se encuentra dentro de la captura del fotograma.
	Esta función devuelve una variable booleana que indica si hay un contorno correspondiente a la mano de los jugadores.
	De esta forma no se utiliza esta imágen para comparar las posiciones de las piezas. 
	"""
	hand = False # Variable booleana que indica la presencia de la mano del jugador

	contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Obtiene los contornos de la imágen

	# Busca un contorno superior a 500, el cual indica la presencia de la mano del jugador dentro de la captura del tablero de ajedrez.
	for contour in contours:
		if cv2.contourArea(contour) > 500:
			hand = True
			break

	return hand


