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
	coordinates = []
	kernel = np.ones((5, 5), np.uint8)

	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	prev_blur = cv2.blur(prev_gray, (29, 29), 1)
	blur = cv2.blur(gray, (29, 29), 1)

	diff = cv2.absdiff(prev_blur, blur)
	diff = cv2.dilate(diff, kernel, iterations = 1)

	h, thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
	hand = detect_hand(thresh)	

	thresh = cv2.erode(thresh, kernel, iterations = 3)
	thresh = cv2.dilate(thresh, kernel, iterations = 3)

	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	list_contours = list(contours)

	print(f'len contours {len(list_contours)}')
	if len(list_contours) == 2 or len(list_contours) == 3:
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

		coordinates.append(c1)
		coordinates.append(c2)	
	elif len(list_contours) >= 4:
		cnt1 = max(list_contours, key = lambda x: cv2.contourArea(x))
		list_contours.remove(cnt1)
	
		cnt2 = max(list_contours, key = lambda x: cv2.contourArea(x))
		list_contours.remove(cnt2)

		cnt3 = max(list_contours, key = lambda x: cv2.contourArea(x))
		list_contours.remove(cnt3)
	
		cnt4 = max(list_contours, key = lambda x: cv2.contourArea(x))

		M1 = cv2.moments(cnt1)
		x1 = int(M1["m10"]/M1["m00"])
		y1 = int(M1["m01"]/M1["m00"])
		c1 = (x1, y1)

		M2 = cv2.moments(cnt2)
		x2 = int(M2["m10"]/M2["m00"])
		y2 = int(M2["m01"]/M2["m00"])
		c2 = (x2, y2)

		M3 = cv2.moments(cnt3)
		x3 = int(M3["m10"]/M3["m00"])
		y3 = int(M3["m01"]/M3["m00"])
		c3 = (x3, y3)

		M4 = cv2.moments(cnt4)
		x4 = int(M4["m10"]/M4["m00"])
		y4 = int(M4["m01"]/M4["m00"])
		c4 = (x4, y4)

		coordinates.append(c1)
		coordinates.append(c2)
		coordinates.append(c3)
		coordinates.append(c4)
	elif len(list_contours) == 3:
		cnt1 = max(list_contours, key = lambda x: cv2.contourArea(x))
		list_contours.remove(cnt1)
	
		cnt2 = max(list_contours, key = lambda x: cv2.contourArea(x))
		list_contours.remove(cnt2)

		cnt3 = max(list_contours, key = lambda x: cv2.contourArea(x))

		M1 = cv2.moments(cnt1)
		x1 = int(M1["m10"]/M1["m00"])
		y1 = int(M1["m01"]/M1["m00"])
		c1 = (x1, y1)

		M2 = cv2.moments(cnt2)
		x2 = int(M2["m10"]/M2["m00"])
		y2 = int(M2["m01"]/M2["m00"])
		c2 = (x2, y2)

		M3 = cv2.moments(cnt3)
		x3 = int(M3["m10"]/M3["m00"])
		y3 = int(M3["m01"]/M3["m00"])
		c3 = (x3, y3)

		coordinates.append(c1)
		coordinates.append(c2)
		coordinates.append(c3)
	
	else:
		coordinates.append((0, 0))

	return coordinates


def check_difference(prev_frame, frame):
	movement = False

	kernel = np.ones((7, 7), np.uint8)
	
	prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	prev_blur = cv2.blur(prev_gray, (29, 29), 1)
	blur = cv2.blur(gray, (29, 29), 1)

	diff = cv2.absdiff(prev_blur, blur)
	diff = cv2.dilate(diff, kernel, iterations = 2)

	h, thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
	contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) != 0:
		movement = True

	return movement


def detect_hand(frame):
	hand = False

	contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in contours:
		if cv2.contourArea(contour) > 500:
			hand = True
			break

	return hand


