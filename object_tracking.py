from __future__ import division
from imutils.video import VideoStream
from collections import deque
import numpy as np 
import argparse
import imutils
import cv2
import time
import RPi.GPIO as IO 

IO.setmode(IO.BOARD)

IO.setup(19,IO.OUT)

dutyCycle = 7.5
p = IO.PWM(19,50)

p.start(dutyCycle)
p.ChangeDutyCycle(7.5)

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to optional video file")
ap.add_argument("-b","--buffer",type = int,default=64,help = "max buffer size")
args = vars(ap.parse_args())

## limits of color detection 
#hsvUpper = (0,90,100)
#hsvLower = (0,100,58)
redLower = [0,0,150]
redUpper = [100,100,255]
lower = np.array(redLower,dtype="uint8")
upper = np.array(redUpper,dtype="uint8")
pts = deque(maxlen=args["buffer"])

#if a video path is not given, select webcam
if not args.get("video",False):
	#camera = cv2.VideoCapture(0)
	camera = VideoStream(src=0).start()
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output2.avi',fourcc,20.0,(640,480))
	time.sleep(2.0)
else:
	camera = cv2.VideoCapture(args["video"])
	

#main loop
while True:
	frame = camera.read()
	#cv2.imshow("Frame",frame)
	if args.get("video") and not grabbed:
		break;

	frame = cv2.resize(frame, (640,480))
#	frame = imutils.resize(frame, height=600)
#	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(frame,lower,upper)
#	mask = cv2.inRange(hsv,hsvLower,hsvUpper)
	mask = cv2.erode(mask,None,iterations=2)
	mask = cv2.dilate(mask,None,iterations=2)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	cv2.circle(frame,(320,240),5,(0,255,0),-1)

	if len(cnts)>0:
		c = max(cnts,key=cv2.contourArea)
		((x,y),radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
		
		
		#print(dutyCycle)
		if radius>10:
			cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
			cv2.circle(frame,center,5,(0,0,255),-1)
			text = center
			cv2.putText(frame,'{} {}'.format(int(x),int(y)),center,cv2.FONT_HERSHEY_SIMPLEX,1.5,255)
			diffX = int(x) - 320
			error = -diffX/600
			angle = 15*error
			dutyCycle = dutyCycle + (angle*10/180)
			print("diffX: %d, angle: %d, error: %d, dutyCycle: %d",(diffX,angle,error,dutyCycle))
			if dutyCycle >=2.5 and dutyCycle<=12.5:
				p.ChangeDutyCycle(dutyCycle)
	pts.appendleft(center)
	cv2.imshow("Frame",mask)
	out.write(mask)
	key = cv2.waitKey(1) & 0xFF
	
	if key==ord('q'):
		break
#camera.release()
camera.stop()
out.release()
cv2.destroyAllWindows()
