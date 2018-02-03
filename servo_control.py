import RPi.GPIO as IO
import time

IO.setwarnings(False)

IO.setmode(IO.BOARD)

IO.setup(19,IO.OUT)

p = IO.PWM(19,50)

p.start(7.5)
p.ChangeDutyCycle(2.5)
dutyCycle = 2.5
x = 0
#for x in range(0,180,5):
#	print(x)	
#	angle = x
#	dutycycle = 2.5+(angle*10/180)
#	p.ChangeDutyCycle(dutycycle)
#	time.sleep(0.5)
while x<=100:
	x=x+0.1
	p.ChangeDutyCycle(dutyCycle)
	
p.ChangeDutyCycle(7.5)
time.sleep(1)
