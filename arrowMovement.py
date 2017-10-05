import numpy as np
import cv2
import pyautogui
import os

l,r,u,d=0,0,0,0


#Move using only the small area
#If cursor goes out of it, click on it using position
#Alt+Tab when done with focus

altNeed=0
cap = cv2.VideoCapture(0)
while(True):
    global l,h,r,d, altNeed
    # Capture frame-by-frame
    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    cv2.rectangle(frame,(250,50),(592,242),(0,0,255),5);
    crop=frame[50:242,250:592]	
    cv2.rectangle(crop,(113,0),(227,63),(0,255,0),1);
    cv2.rectangle(crop,(0,65),(113,127),(0,255,0),1);
    cv2.rectangle(crop,(113,127),(227,191),(0,255,0),1);
    cv2.rectangle(crop,(229,65),(341,127),(0,255,0),1);
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
 
    #color definitions
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([120,255,255])
    mask_blue= cv2.inRange(hsv, lower_blue, upper_blue)
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)

    cv2.imshow('Blue',mask_blue)
    cv2.moveWindow("Blue",100,100)
   
   
    #To find contours
    #BLUE
    cnts_blue = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts_blue) > 0:
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
		if center_blue[0]>=113 and center_blue[0]<227:
			if center_blue[1]>=0 and center_blue[1]<63:
				u+=1
				l,r,d=0,0,0				
				if u>=5:
#					print "UP"
					pyautogui.press("up")
					u=0
		if center_blue[0]>=0 and center_blue[0]<112:
			if center_blue[1]>=65 and center_blue[1]<128:
				l+=1
				r,u,d=0,0,0
				if l>=5:
#					print "LEFT"
					pyautogui.press("left")
					l=0
		if center_blue[0]>=229 and center_blue[0]<341:
			if center_blue[1]>=65 and center_blue[1]<128:
				r+=1
				l,u,d=0,0,0
				if r>=5:
#					print "RIGHT"
					pyautogui.press("right")
					r=0
		if center_blue[0]>=113 and center_blue[0]<227:
			if center_blue[1]>=128 and center_blue[1]<192:
				d+=1
				r,u,l=0,0,0
				if d>=5:
					pyautogui.press("down")
#					print "DOWN"
					d=0
    else:
			
			#Find cursor in window and alt+tab		
			altNeed=-8
			os.system("wmctrl -a Blue")
			
    # Display the resulting frame
    cv2.imshow('frame',frame)
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

