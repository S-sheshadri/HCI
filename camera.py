import cv2
import numpy as np
import pyautogui

def mapx(x):
   y=(x)/(639)*(392-50)+50
   return y
def mapy(y):
   z=(y)/(479)*(242-50)+50
   return z
cap = cv2.VideoCapture(00)

if cap==None:exit()

while(1):

    # Take each frame
    _, frame = cap.read()
    frame=cv2.flip(frame,1)
    cv2.rectangle(frame,(250,50),(592,242),(0,0,255),5);
    crop=frame[50:242,250:592]	
    # Convert BGR to HSV
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    #print cap.get(3)
    #To get value from file
    """file=open("blueHue","r")
    values=file.readlines()
    lower_hue=int(values[0])
    upper_hue=int(values[1])
    if lower_hue>upper_hue:
		if 360-lower_hue<upper_hue:
			lower_hue=0
		else:
			upper_hue=360
    # define range of blue color in HSV
    """
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([120,255,255])
    lower_green = np.array([45,50,50])
    upper_green = np.array([85,255,255])
    lower_red= np.array([0,50,50])
    upper_red = np.array([10,255,255])
	
    # Threshold the HSV image to get only blue colors
    mask_blue= cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green= cv2.inRange(hsv, lower_green, upper_green)
    mask_red= cv2.inRange(hsv, lower_red, upper_red)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.dilate(mask_red, None, iterations=2)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)
    
    """# Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
    ret,thresh = cv2.threshold(blurred,127,255,0)
    contours, _ = cv2.findContours(blurred.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    centres=[]
    for i in range(len(contours)):
		  moments = cv2.moments(contours[i])
		  if(not moments['m00']==0):
				centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
		  		cv2.circle(blurred, centres[-1], 3, (0, 0, 0), -1)
	"""
    # show the image
    #cv2.waitKey(0)
    cv2.imshow('frame',frame)
    cv2.imshow('BLUE',mask_blue)
    cv2.imshow('GREEN',mask_green)
    cv2.imshow('RED',mask_red)
	
    #To find contours
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
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
           break

cv2.destroyAllWindows()

#blue moves cursor
#blue + green clicks
#blue + red? double clicks
