import cv2
import numpy as np
import pyautogui

def mapx(x):
   y=(x)/(639)*(392-50)+50
   return y
def mapy(y):
   z=(y)/(479)*(242-50)+50
   return z
cap = cv2.VideoCapture(0)

if cap==None:exit()

while(1):

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
		pyautogui.moveTo(center_blue[0]*4,center_blue[1]*4)
    ####################
    #GREEN
    cnts_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_green = None
    if len(cnts_green) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts_green, key=cv2.contourArea)
		M = cv2.moments(c)
		center_green = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		#if not (center_blue == None) and not (center_green == None) :print (center_blue[0]-center_green[0])**2+(center_blue[1]-center_green[1])**2
    		if not (center_blue == None) and (center_blue[0]-center_green[0])**2+(center_blue[1]-center_green[1])**2<1000:	pyautogui.click(center_blue[0]*4,center_blue[1]*4)
    
    #PURPLE
    cnts_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center_red = None
    isDrag=False
    if len(cnts_red) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts_red, key=cv2.contourArea)
		M = cv2.moments(c)
		center_red = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
   		if not (center_blue == None) and (center_blue[0]-center_red[0])**2+(center_blue[1]-center_red[1])**2<1000:  
			isDrag=True
	        pyautogui.mouseDown(center_blue[0],center_blue[1])
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
