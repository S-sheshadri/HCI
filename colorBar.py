import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('LOW HUE','image',0,360 ,nothing)
cv2.createTrackbar('HIGH HUE','image',0,360,nothing)
cv2.createTrackbar('LOW S','image',0,255,nothing)
cv2.createTrackbar('HIGH S','image',0,255,nothing)
cv2.createTrackbar('LOW V','image',0,255,nothing)
cv2.createTrackbar('HIGH V','image',0,255,nothing)


cap = cv2.VideoCapture(0)
if cap==None:exit()
while(1):

    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # get current positions of four trackbars
    lh = cv2.getTrackbarPos('LOW HUE','image')
    hh = cv2.getTrackbarPos('HIGH HUE','image')
    ls = cv2.getTrackbarPos('LOW S','image')
    hs= cv2.getTrackbarPos('HIGH S','image')
    lv= cv2.getTrackbarPos('LOW V','image')
    hv= cv2.getTrackbarPos('HIGH V','image')
	
    # define range of blue color in HSV
    lower_blue = np.array([lh,ls,lv])
    upper_blue = np.array([hh,hs,hv])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #green = np.uint8([[[0,255,0 ]]])
    bgr = cv2.cvtColor(np.uint8([[[lh,lv,ls]]]),cv2.COLOR_HSV2BGR)
    print bgr
    #img[:] = bgr    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.waitKey()

    
    ####################
   

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
           break

cv2.destroyAllWindows()

cv2.destroyAllWindows()