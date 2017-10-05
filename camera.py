import cv2
import numpy as np
import pyautogui
import os

#Set Mode
# Cursor Mode
# Shortcut mode

cap = cv2.VideoCapture(0)
print cap
if cap==None:exit()

#Old cursor points
oldx=0
oldy=0
altNeed=0
#To check if its first time
first=1

while(1):
    global oldx,oldy,altNeed
    # Take each frame
    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    cv2.rectangle(frame,(250,50),(592,242),(0,0,255),5);
    crop=frame[50:242,250:592]	
    # Convert BGR to HSV
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    
    #color definitions
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([120,255,255])
    lower_green = np.array([45,50,50])
    upper_green = np.array([85,255,255])
    lower_red= np.array([150,70,50])#actually purple
    upper_red = np.array([179,250,250])
    lower_yellow=np.array([15, 150, 150])	
    upper_yellow=np.array([65, 255, 255])
	
    mask_blue= cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green= cv2.inRange(hsv, lower_green, upper_green)
    mask_red= cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow= cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.dilate(mask_red, None, iterations=2)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)
    mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
    mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)
    
    # show the image
    cv2.imshow('frame',frame)
    cv2.imshow('BLUE',mask_blue)
    cv2.imshow('GREEN',mask_green)
    cv2.imshow('RED',mask_red)
    cv2.imshow('YELLOW',mask_yellow)
    
    #adjust window positions
    cv2.moveWindow('BLUE',683,50)
    cv2.moveWindow('GREEN',1025,50)
    cv2.moveWindow('YELLOW',683,292)
    cv2.moveWindow('RED',1025,292)
    cv2.moveWindow('Frame',100,100)

    #To find contours
    #BLUE
    cnts_blue = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_blue = None
    if len(cnts_blue) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		
		# centroid
		if first==1:
			print "FTS"
			first=0
		else:
			if altNeed<0:
				altNeed+=1
				if altNeed==0:
					pyautogui.keyDown('alt')
					pyautogui.press('tab')
					pyautogui.keyUp('alt')
	#				print "Alt tab"
	
		c = max(cnts_blue, key=cv2.contourArea)
		M = cv2.moments(c)
		center_blue = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				
		if((oldx-center_blue[0])**2+(oldy-center_blue[1])**2)>1000:
				oldx=center_blue[0]*4
				oldy=center_blue[1]*4
				pyautogui.moveTo(center_blue[0]*4-10,center_blue[1]*4-10)
				
		else:
		        	print oldx,oldy
				print center_blue
    else:
		#Find cursor in window and alt+tab		
			altNeed=-8
			os.system("wmctrl -a BLUE")
    #GREEN
    cnts_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_green = None
    if len(cnts_green) > 0:
		c = max(cnts_green, key=cv2.contourArea)
		M = cv2.moments(c)
		center_green = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    		if not (center_blue == None) and (center_blue[0]-center_green[0])**2+(center_blue[1]-center_green[1])**2<1000:	pyautogui.click(center_blue[0]*4,center_blue[1]*4)
    
    #PURPLE
    cnts_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_red = None
    isDrag=False
    if len(cnts_red) > 0:
		c = max(cnts_red, key=cv2.contourArea)
		M = cv2.moments(c)
		center_red = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if isDrag and (center_blue[0]-center_red[0])**2+(center_blue[1]-center_red[1])**2>1000:
			isDrag=False
			pyautogui.dragTo(center_blue[0],center_blue[1])
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
           break

cv2.destroyAllWindows()

#blue moves cursor
#blue + green clicks
#blue + red? double clicks
