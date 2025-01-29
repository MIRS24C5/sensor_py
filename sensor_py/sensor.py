import RPi.GPIO as GPIO
import time
import sys
import serial

trig_pin = 15
echo_pin = 14
speed_of_sound = 34370

distance = 0.0

ser = serial.Serial('/dev/ttyACM0', 9600)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

time.sleep(2)

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
		distance = get_distance()
		print("Distance: {:.1f} cm".format(distance))
		send_str = f"{distance:.2f}\n"
		ser.write(send_str.encode('utf-8'))
		time.sleep(1)
		
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit()
