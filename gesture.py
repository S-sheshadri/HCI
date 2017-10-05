import cv2
import numpy as np
import pyautogui
import threading
import time
import sched
import os
import sys
#Set Mode
# Cursor Mode
# Shortcut mode

cap = cv2.VideoCapture(0)

if cap==None:exit()

#Old cursor points
oldx=0
oldy=0
startx=0
starty=0
count=0
points=[]
startSet=False
endx,endy=0,0
endSet=False   
newGest=True
count=0
hover=False
notVisible=0
cantSee=False
distance=0
cnts_blue=None

s = sched.scheduler(time.time, time.sleep)
s1 = sched.scheduler(time.time, time.sleep)
	
def callSched():
	while(1):
		s.enter(1, 1, checkHover, ())
		s.run()
		s1.enter(1, 1, checkVisible, ())
		s1.run()

def checkHover():
	global hover, count, distance
	if distance < 100:
		count+=1
	if count>=2:
		count=0
		hover=True
	print count
	#threading.Timer(1.0,checkHover).start()


def checkVisible():
	global notVisible, cnts_blue,cantSee,count 
	if not cnts_blue==None and len(cnts_blue)==0:
		notVisible+=1 
	if notVisible>=2:
		count=0
		cantSee=True
		notVisible=0
	#threading.Timer(1.0,checkVisible).start()



threading.Timer(1.0,callSched).start()


#Call tracker
#checkHover()
#checkVisible()
while(1):
    global distance, cnts_blue, count
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
    mask_blue = cv2.erode(mask_blue, None, iterations=2)
    mask_blue = cv2.dilate(mask_blue, None, iterations=2)
    
    # show the image
    cv2.imshow('frame',frame)
    cv2.imshow('BLUE',mask_blue)
    
    cv2.moveWindow('BLUE',683,50)
    cv2.moveWindow('Frame',100,100)
    
    #To find contours
    #BLUE
    cnts_blue = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts_blue) > 0:
		c = max(cnts_blue, key=cv2.contourArea)
		M = cv2.moments(c)
		center_blue = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if newGest:
				if hover and not startSet:
					startx=center_blue[0]
					starty=center_blue[1]
					count=0
					startSet=True
					hover=False
					os.system("paplay /usr/share/sounds/ubuntu/stereo/dialog-information.ogg")
				if startSet and hover:
					#check if its still near start
					if (startx-center_blue[0])**2+(starty-center_blue[1])**2>150:
						count=0
						startSet=False
						endx=center_blue[0]
						endy=center_blue[1]
						endSet=True
						hover=False
						os.system("paplay /usr/share/sounds/ubuntu/stereo/bell.ogg")	
						newGest=False
		distance = ((oldx-center_blue[0])**2+(oldy-center_blue[1])**2)
		oldx=center_blue[0]
		oldy=center_blue[1]
    if cantSee:
		newGest=True
		cantSee=False
		startSet=False
		count=0
		os.system("paplay /usr/share/sounds/ubuntu/stereo/message.ogg")
    if endSet:
	print (endx-startx),abs(starty-endy)
	#switch case
	if (endx-startx)>100 and abs(starty-endy)<20:
		print "Left to right"
		pyautogui.press("right")
	elif (startx-endx)>100 and abs(starty-endy)<20:
		print "Right to left"
		pyautogui.press("left")
	elif (endy-starty)>80 and abs(startx-endx)<15:
		print "Up to down"
	elif (starty-endy)>80 and abs(startx-endx)<15:
		print "Down to up"
	endSet=False
    	count=0			
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
           sys.exit()

cv2.destroyAllWindows()

#blue moves cursor
#blue + green clicks
#blue + red? double clicks
