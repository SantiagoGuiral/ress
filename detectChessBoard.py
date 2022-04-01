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
	xSorted = pts[np.argsort(pts[:, 0]), :]

	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]

	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost

	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]

	return [tl, tr, bl, br]


def get_chessboardcorners(img):
	corners = []
	found, c = cv2.findChessboardCorners(img, (7, 7))
	
	for corner in c:
		corners.append(list(c[0]))
	return found, corners


def get_chessboardborders(img):
	tinf, tsup =  25, 60
	kernel = np.ones((3, 3), np.uint8)

	image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	image = cv2.GaussianBlur(image, (3, 3), 1)
	image = cv2.Canny(image, tinf, tsup)
	image = cv2.dilate(image, kernel, iterations = 2)
	return image


def get_chessboardcontour(img):
	contoursmax = []

	contours, h = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	cntmax = max(contours, key = lambda x: cv2.contourArea(x))
	return cntmax


def get_chessboardhull(img, cntmax):
	kernel = np.ones((3, 3), np.uint8)
	hull = []
	
	drawing = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
	color = (255, 255, 255)

	hull.append(cv2.convexHull(cntmax, False))
	cv2.drawContours(drawing, hull, -1, color, 1, 16)
	image = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)

	contours, h = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)	
	return contours, image


def get_chessboardcoordinates(img, contours):
	for contour in contours:
		epsilon = 0.1 * cv2.arcLength(contour, True)
		borders = cv2.approxPolyDP(contour, epsilon, True) 

	if len(borders) == 4:
		borders = np.array([list(borders[0][0]), list(borders[1][0]), list(borders[2][0]), list(borders[3][0])])
		borders = order_points(borders)
	else:
		borders = None

	return borders


def get_chessboardrect(cntmax):
	(x, y, w, h) = cv2.boundingRect(cntmax)
	corners = [[x, y],[x+w, y],[x, y+h],[x+w, y+h]]
	return corners, w, h


def get_perspective(pts_init, pts_final, w, h, img):
	pts_init = np.float32(pts_init)
	pts_final = np.float32([[0,0],[w,0],[0,h],[w,h]])

	M = cv2.getPerspectiveTransform(pts_init, pts_final)
	image = cv2.warpPerspective(img, M, (w, h))
	return image

