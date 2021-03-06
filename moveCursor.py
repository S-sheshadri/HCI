import cv2
import numpy as np
import pyautogui
cap = cv2.VideoCapture(0)
if cap==None:exit()
while(1):

    # Take each frame
    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
    #To get value from file
    file=open("blueHue","r")
    values=file.readlines()
    lower_hue=int(values[0])
    upper_hue=int(values[1])
    lower_sat=int(values[2])
    upper_sat=int(values[3])
    lower_val=int(values[4])
    upper_val=int(values[5])

    if lower_hue>upper_hue:
		if 180-lower_hue<upper_hue:
			lower_hue=0
		else:
			upper_hue=180
    if lower_sat>upper_sat:
        if 256-lower_sat<upper_sat:
            lower_sat=0
        else:
            upper_sat=256
    if lower_val>upper_val:
        if 256-lower_val<upper_val:
            lower_val=0
        else:
            upper_val=256

    # define range of blue color in HSV
    lower_blue = np.array([93,97,53])
    upper_blue = np.array([180,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
    ret,thresh = cv2.threshold(blurred,127,255,0)
    contours, _ = cv2.findContours(blurred.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    centres=[]
    for i in range(min(1,len(contours))):#len(contours)):
		  moments = cv2.moments(contours[i])
		  if(not moments['m00']==0):
				centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
		  		cv2.circle(blurred, centres[-1], 3, (0, 0, 0), -1)
   				#get center and move cursor
				pyautogui.moveTo(centres[-1][0],centres[-1][1])
    
    # show the image
    #cv2.waitKey(0)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',blurred)
    

    
    ####################
   

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
           break

cv2.destroyAllWindows()
