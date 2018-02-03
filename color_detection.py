# import packages
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",help="/home/farhan/Downloads/red-ball-in-snow.jpg")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

#defining boundaries
#lowerRange = [25,25,100]
lowerRange = [0,0,50]
upperRange = [100,100,255]

lower = np.array(lowerRange,dtype="uint8")
upper = np.array(upperRange,dtype="uint8")

mask = cv2.inRange(image,lower,upper)
output = cv2.bitwise_and(image,image,mask=mask)

cv2.imshow("images",np.hstack([image,output]))
cv2.waitKey(0)
