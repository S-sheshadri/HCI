import cv2
import numpy as np
import pyautogui
import os

#Set Mode
# Cursor Mode
# Shortcut mode

cap = cv2.VideoCapture(0)

if cap==None:exit()
l,r,u,d=0,0,0,0

#Old cursor points
oldx=0
oldy=0
mode = 0 #cursor mode
redThere=0
while(1):
    global oldx,oldy, cursor, redThere, l,h,r,d, altNeed
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
    lower_green = np.array([45,50,50])
    upper_green = np.array([85,255,255])
    lower_red= np.array([150,50,50])#actually purple
    upper_red = np.array([179,255,255])
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

    #If mode is cursor
    if (mode==0):
	    #To find contours
	    #BLUE

	    cnts_blue = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	    center_blue = None
	    if len(cnts_blue) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
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
	    if len(cnts_red) > 0:
		redThere+=1
		if redThere>=4:
			redThere=-4
			mode=(mode+1)%2
			print "chenhe", mode

    elif mode==1:
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
#PURPLE
			    cnts_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
			    if len(cnts_red) > 0:
				redThere+=1
				if redThere>=4:
					redThere=-4
					mode=(mode+1)%2
					print "CHANGING MODE" , mode



    k = cv2.waitKey(5) & 0xFF
    if k == 27:
           break

cv2.destroyAllWindows()

#blue moves cursor
#blue + green clicks
#blue + red? double clicks
