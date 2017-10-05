import cv2
import numpy 

hsvColor=None
lower_hue=None
lower_val=None
lower_sat=None
upper_sat=None
upper_val=None
upper_hue=None
cap = cv2.VideoCapture(0)

if cap==None:exit()

def takePhoto():
	global lower_val, upper_val, lower_sat, upper_sat, hsvColor, lower_hue, upper_hue
	cv2.waitKey(0)
	# Take each frame
	_, frame = cap.read()
	height=len(frame)
	width=len(frame[0])
	y=height*.40
	yEnd=height*.60
	x=width*.40
	xEnd=width*.60
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
	#print "HSV",hsvColor ,"lower_hue",(hsvColor[0][0][0]-30)%360
	lower_hue=(hsvColor[0][0][0]-15)%180
	upper_hue=(hsvColor[0][0][0]+15)%180
	lower_sat=(hsvColor[0][0][1]-15)%256
	upper_sat=(hsvColor[0][0][1]+15)%256
	lower_val=(hsvColor[0][0][2]-15)%256
	upper_val=(hsvColor[0][0][2]+15)%256

	#to write into file
	file=open("blueHue","w")
	file.write(str(lower_hue))
	file.write("\n")
	file.write(str(upper_hue))
	file.write("\n")
	file.write(str(lower_sat))
	file.write("\n")
	file.write(str(upper_sat))
	file.write("\n")
	file.write(str(lower_val))
	file.write("\n")
	file.write(str(upper_val))
	file.close()
	cv2.imshow("original",frame)
	cv2.imshow("cropped", croppedFrame)
	cv2.waitKey(0)

takePhoto()		


while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if lower_hue>upper_hue:
		if 360-lower_hue<upper_hue:
			lower_hue=0
		else:
			upper_hue=360
    # define range of blue color in HSV
    lower_blue = numpy.array([lower_hue,50,50])
    upper_blue = numpy.array([upper_hue,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)


    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)



    #######################


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


