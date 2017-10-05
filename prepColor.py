import cv2
import numpy as np
import pyautogui


#To see if colors are visible

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
    cv2.moveWindow('Frame',100,100)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
           break

