import cv2
import numpy as np

url = "https://10.1.143.75:8080/video"

cap = cv2.VideoCapture(url)

while(True):
	camera, frame = cap.read()
	resize = cv2.resize(frame, (600,400))
	cv2.imshow("Frame", resize)
    
	q = cv2.waitKey(1)
	if q==ord("q"):
		break


cv2.destroyAllWindows()
