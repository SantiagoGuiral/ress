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

import numpy as np
import cv2
from scipy.spatial import distance as dist

def order_points(pts):
	""" Ordena las coordenadas del tablero de ajedrez desde la esquina superior izquierda hasta la esquina inferior derecha 
	con el objetivo de asociar correctamente las coordenadas reales con las coordenadas que permiten obtener la perspectiva del tablero.
	"""
	xSorted = pts[np.argsort(pts[:, 0]), :] # Ordena las coordendas horizontalmente

	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]

	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost

	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]

	return [tl, tr, bl, br] # coordenadas ordenadas


def get_chessboardborders(img):
	""" Obtiene los bordes de la imagen capturada, la cual será usada para detectar el contorno del tablero. 
	Recibe como entrada la imagen del tablero vacío y la salida es la imagen con los bordes detectados mediante la técnica Canny.
	"""
	tinf, tsup =  25, 60 # Limites de la derivada para hallar los bordes
	kernel = np.ones((3, 3), np.uint8) # Elemento estructurante para el proceso morfológico

	image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convierte la imágen en escala de grises
	image = cv2.GaussianBlur(image, (3, 3), 1) # Aplica un filtro para suavizar la imágen
	image = cv2.Canny(image, tinf, tsup) # Encuentra los bordes de la captura de acuerdo a los limites del contorno
	image = cv2.dilate(image, kernel, iterations = 2) # Dilata los bordes obtenidos
	return image


def get_chessboardcontour(img):
	"""Obtiene los contornos que hay en la imágen que posee todos los bordes detectados con Canny.
	La salida es el contorno de mayor tamaño que corresponde al tablero de ajedrez.
	"""
	contours, h = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Encuentra los contornos en la imágen
	cntmax = max(contours, key = lambda x: cv2.contourArea(x)) # Encuentra el contorno de mayor tamaño 
	return cntmax


def get_chessboardhull(img, cntmax):
	"""Genera un polígono convexo a partir del contorno correspondiente al tablero de ajedrez.
	Recibe la imagen del tablero y el contorno correspondiente al tablero.
	La salida es el contorno del nuevo polígono y la imágen generada para este polígono.
	"""
	kernel = np.ones((3, 3), np.uint8) # Elemento estructurante
	hull = []
	
	drawing = np.zeros((img.shape[0], img.shape[1], 3), np.uint8) # Matrix para dibujar el polígono del tablero
	color = (255, 255, 255) # Color del poligono

	hull.append(cv2.convexHull(cntmax, False)) # Polígono del tablero
	cv2.drawContours(drawing, hull, -1, color, 1, 16) # Dibuja el polígono que representa al contorno en la nueva imágen
	image = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY) # Convierte a escala de grises

	contours, h = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)	# Encuentra el contorno del único poligono en la imágen
	return contours, image


def get_chessboardcoordinates(img, contours):
	"""Establece un polígono convexo y extrae las coordenadas de los cuatro vértices en el contorno del tablero.
	La entrada es la imágen con el polígono dibujado y el contorno que lo representa.
	La salida es una lista con las coordenadas de las esquinas del tablero de ajedrez.
	Estas coordenadas séran usadas para delimitar la detección de movimiento solamente en los pixeles que representan el tablero.
	"""
	# Obtiene los bordes del polígono del tablero
	for contour in contours:
		epsilon = 0.1 * cv2.arcLength(contour, True) # Establece la curvatura limite que determina los 4 bordes del tablero
		borders = cv2.approxPolyDP(contour, epsilon, True) # Coordenadas de los vertices

	# Organiza las coordenadas en un array de Numpy
	if len(borders) == 4:
		borders = np.array([list(borders[0][0]), list(borders[1][0]), list(borders[2][0]), list(borders[3][0])])
		borders = order_points(borders) # Organiza las coordenadas en orden para luego obtener la perspectiva correcta.
	else:
		borders = None

	return borders


def get_chessboardrect(cntmax):
	"""Obtiene los bordes del polígono ideal que representa el tablero de ajedrez. Para esto recibe el contorno de mayor área y obtiene
	la coordenada del punto superior izquierdo con el ancho y el alto. A partir de estos valores se obtiene el tamaño idealizado del
	tablero de ajedrez para sacar una perspectiva vertical. La salida es las cuatro coordenadas de los vértices.
	"""
	(x, y, w, h) = cv2.boundingRect(cntmax) # Obtiene un vertice y el tamaño del contorno
	corners = [[x, y],[x+w, y],[x, y+h],[x+w, y+h]] # Genera las coordenadas para los cuatro vertices del tablero
	return corners, w, h


def get_perspective(pts_init, pts_final, w, h, img):
	"""Obtiene una imágen con perspectiva vertical de tablero de ajedrez. Para esto recibe las coordenadas obtenidas del polígono generado
	desde la captura del tablero de ajedrez y también recibe las coordenadas de un polígono ideal. Con estos valores se transforma la
	imágen para obtener una imágen que se ve desde una perspectiva superior.
	"""
	pts_init = np.float32(pts_init) # Coordenadas de los vertices desde la captura original del tablero
	pts_final = np.float32([[0,0],[w,0],[0,h],[w,h]]) # Nuevas coordenadas que tendra la imágen con perspectiva vertical.

	M = cv2.getPerspectiveTransform(pts_init, pts_final) # Genera la matriz de de transformación al asociar las coordenadas
	image = cv2.warpPerspective(img, M, (w, h)) # Obtiene una nueva imágen con la perspectiva vertical
	return image

