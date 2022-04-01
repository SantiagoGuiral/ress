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
	kernel = np.ones((7, 7), np.uint8)
	
	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	prev_blur = cv2.blur(prev_gray, (29, 29), 1)
	blur = cv2.blur(gray, (29, 29), 1)

	diff = cv2.absdiff(prev_blur, blur)
	diff = cv2.dilate(diff, kernel, iterations = 2)

	h, thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
	hand = detect_hand(thresh)	

	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) >= 2:
		list_contours = list(contours)
		cnt1 = max(list_contours, key = lambda x: cv2.contourArea(x))
		list_contours.remove(cnt1)
	
		cnt2 = max(list_contours, key = lambda x: cv2.contourArea(x))
	
		M1 = cv2.moments(cnt1)
		x1 = int(M1["m10"]/M1["m00"])
		y1 = int(M1["m01"]/M1["m00"])
		c1 = (x1, y1)

		M2 = cv2.moments(cnt2)
		x2 = int(M2["m10"]/M2["m00"])
		y2 = int(M2["m01"]/M2["m00"])
		c2 = (x2, y2)
	else:
		c1 = (0, 0)
		c2 = (0, 0)

	return c1, c2, thresh


def detect_hand(frame):
	hand = False

	contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in contours:
		if cv2.contourArea(contour) > 500:
			hand = True
			break

	return hand


