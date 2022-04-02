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
	kernel = np.ones((3, 3), np.uint8)
	motion = False
	
	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	prev_blur = cv2.GaussianBlur(prev_gray, (5, 5), 1)
	blur = cv2.GaussianBlur(gray, (5, 5), 1)

	diff = cv2.absdiff(prev_blur, blur)
	h, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
	dilated = cv2.dilate(thresh, kernel, iterations = 1)
	contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	for contour in contours:
		if cv2.contourArea(contour) > 30:
			motion = True
			break

	return motion
