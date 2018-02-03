from __future__ import division 

x = 500
dutyCycle = 10
diffX = int(x) - 320
error = -diffX/600
angle = 30*error
dutyCycle = dutyCycle + (angle*10/180)
print("diffX: %d, angle: %d, error: %d, dutyCycle: %d",(diffX,angle,error,dutyCycle))
if dutyCycle >=2.5 and dutyCycle<=12.5:
	print("YES!!")
else:
	print("NO!")
