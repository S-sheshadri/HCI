import cv2
import numpy 

hsvColor=None
cap = cv2.VideoCapture(0)

if cap==None:exit()

def takePhoto():
	cv2.waitKey(0)
	# Take each frame
	_, frame = cap.read()
	height=len(frame)
	width=len(frame[0])
	y=height*.25
	yEnd=height*.75
	x=width*.25
	xEnd=width*.75
	#crop to get center
	croppedFrame =frame[y:yEnd,x:xEnd] 
	# Crop from x, y, w, h -> 100, 200, 300, 400
	#NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
		
	#To get average of color
	average_color_per_row = numpy.average(croppedFrame, axis=0)
	average_color = numpy.average(average_color_per_row, axis=0)
	print average_color
	
	#To get color for HSV
	average_color=numpy.uint8([[average_color]])
	hsvColor=cv2.cvtColor(average_color,cv2.COLOR_BGR2HSV)	
	
	cv2.imshow("original",frame)
	cv2.imshow("cropped", croppedFrame)
	cv2.waitKey(0)
takePhoto()		
lower_hue=hsvColo[0]
while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # define range of blue color in HSV
    lower_blue = np.array([,50,50])
    upper_blue = np.array([110,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)


    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    #cv2.imshow('res',res)



    #######################


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
"""

