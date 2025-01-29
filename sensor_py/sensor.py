import RPi.GPIO as GPIO
import time
import sys

trig_pin = 15
echo_pin = 14
speed_of_sound = 34370

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

print('now running...')

def get_distance():
	GPIO.output(trig_pin, GPIO.HIGH)
	time.sleep(0.000010)
	GPIO.output(trig_pin, GPIO.LOW)
	
	while not GPIO.input(echo_pin):
		pass
	t1 = time.time()
	
	while GPIO.input(echo_pin):
		pass
	t2 = time.time()
	
	return (t2 - t1) * speed_of_sound / 2
	
while True:
	try:
		distance = '{:.1f}'.format(get_distance())
		print("Distance: " + distance + "cm")
		time.sleep(1)
		
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit()
