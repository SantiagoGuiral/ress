import numpy as np
import cv2

def get_chessboardcorners(img):
	found, corners = cv2.findChessboardCorners(img, (7, 7))
	return found, corners

def get_chessboardborders(img):
	tinf, tsup =  200, 400
	kernel = np.ones((3, 3), np.uint8)

	imgage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	image = cv2.GaussianBlur(image, (3, 3), 1)
	image = cv2.Canny(image, tinf, tsup)
	return image

def get_chessboardcontour(img):
	contoursmax = []

	contours, h = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	cntmax = max(contours, key = lambda x: cv2.contourArea(x))
	contoursmax.append(cntmax)
	return contoursmax

def get_chessboardrect(contours):
	borders = []
	(x, y, w, h) = cv2.boundingRect(contours[0])
	borders.append([x,y])
	borders.append([x+w,y])
	borders.append([x,y+h])
	borders.append([x+w,y+h])
	return borders

def get_chessboardhull(img, cntmax):
	hull = []
	kernel = np.ones((3, 3), np.uint8)

	image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
	hull.append(cv2.convexHull(cntmax, False))
	cv2.drawContours(image, hull, -1, (255, 255, 255), 1, 16)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	contours, h = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	return contours

def get_chessboardcoordinates(img, contours):
	for contour in contours:
		epsilon = 0.001 * cv2.arcLength(contour, True)
		borders = cv2.approxPolyDP(contour, epsilon, True) 
	return borders

