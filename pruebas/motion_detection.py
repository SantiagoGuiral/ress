"""
----------SANTIAGO RIOS GUIRAL--------------------------------------------------
----------santiago.riosg@udea.edu.co--------------------------------------------
--------------------------------------------------------------------------------
----------EMMANUEL GOMEZ OSPINA-------------------------------------------------
----------emmanuel.gomezo@udea.edu.co-------------------------------------------
--------------------------------------------------------------------------------
----------Curso Básico de Procesamiento de Imágenes y Visión Artificial---------
--------------------------------------------------------------------------------
----------Basado en tutorial:---------------------------------------------------
----------https://gist.github.com/pknowledge/623515e8ab35f1771ca2186630a13d14---
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

import cv2
import numpy as np


url = 0 #'http://192.168.0.4:8080/video'
cap = cv2.VideoCapture(url) # Abre el archivo de video para capturar con la cámara


frame_width = int( cap.get(3)) # Ancho de la imágen capturada por la cámara
frame_height =int( cap.get(4)) # Alto de la imágen capturada por la cámara



# Captura consecutiva de la imágen
ret, frame1 = cap.read() # Captura del primer pantallazo
ret, frame2 = cap.read() # Captura del segundo pantallazo

kernel = np.ones((3, 3), np.uint8) # Elemento estructurante para la dilatación

while cap.isOpened():
	diff = cv2.absdiff(frame1, frame2) # Obtiene la diferencia entre las 2 capturas - restar
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # Conversión de RGB al espacio de grises
	blur = cv2.GaussianBlur(gray, (5,5), 0) # Eliminación del ruido
	h, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) # Binariza la diferencia
	dilated = cv2.dilate(thresh, kernel, iterations=1) # Agranda la mascara
	contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Encuentra todos los contornos de las mascaras que representan el movimiento

	# Recorre los contornos para dibujar un recuadro sobre ellos
	for contour in contours:
		(x, y, w, h) = cv2.boundingRect(contour) # Obtiene las coordenadas del contorno

		#Discrimina el dibujo de rectangulos cuando el movimiento es muy pequeño
		if cv2.contourArea(contour) < 200:
			continue
		cv2.rectangle(frame1, (x, y), (x+w, y+h), (255, 0, 0), 2) # Dibuja el rectangulo
		cv2.putText(frame1, "{}".format('Movement'), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) # Escribe que hay movimiento en la captura

	cv2.imshow("Camera", frame1)
	cv2.imshow("threshold", thresh)

	frame1 = frame2 # Alternamos la imágen que se captura para una nueva comparación
	ret, frame2 = cap.read() # Se obtiene una nueva captura de imágen

	key = cv2.waitKey(1)
	if key == 27:
		break

cv2.destroyAllWindows()
cap.release()
