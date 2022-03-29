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


def difference(prev_frame, frame):
	kernel = np.ones((7, 7), np.uint8)
	
	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	prev_blur = cv2.blur(prev_gray, (29, 29), 1)
	blur = cv2.blur(gray, (29, 29), 1)

	diff = cv2.asdiff(prev_blur, blur)
	diff = cv2.dilate(diff, kernel, iterations = 2)

	h, tresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
	contours = get_contours(thresh)

	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
