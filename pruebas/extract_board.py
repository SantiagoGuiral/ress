import cv2
import numpy as np
import matplotlib.pyplot as plt
import detectChessBoard as dcb

def recognize_board(cframe):
	global board, rect, borders
	capture_frame = cframe.copy()
	image1 = dcb.get_chessboardborders(capture_frame)
	contour = dcb.get_chessboardcontour(image1)
	rect, w, h = dcb.get_chessboardrect(contour)
	contours, image2 = dcb.get_chessboardhull(image1, contour)
	borders = dcb.get_chessboardcoordinates(image2, contours)

	if borders == None:
		print("State: Not Succesful")
	else:
		if (len(borders) == 4 and len(rect) == 4):
			board = dcb.get_perspective(borders, rect, w, h, cframe)
			print("State: Succesful")

			plt.imshow(board)
			plt.savefig('board.png')
			print(f'borders cv2: {borders}')
			print(f'rect {rect}')

		else:
			print("State: Not Succesful")


url = "video.mp4"

cap = cv2.VideoCapture(url)
cnt = 0

while cap.isOpened():

	ret, frame = cap.read() # Se obtiene una nueva captura de imágen

	if cnt == 10:
		recognize_board(frame)

	if ret == True:
		cv2.imshow("Camera", frame)

	cnt+=1

	key = cv2.waitKey(1)
	if key == 27:
		break


cv2.destroyAllWindows()
cap.release()
