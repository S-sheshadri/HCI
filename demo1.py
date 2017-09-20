import numpy as np
import cv2

cap = cv2.VideoCapture(2)


while(1):
	frame,img_test = cap.read()
	#define color range for object detection
	step = 10
	r,g,b = 203, 31, 25 #red
	lower_bgr = np.uint8([b-step, g-step, r-step])
	upper_bgr = np.uint8([b + step, g + step, r + step])

	mask = cv2.inRange(frame, lower_bgr, upper_bgr)
	cv2.imshow('mask', mask)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

    
cv2.destroyAllWindows()
cap.release()
