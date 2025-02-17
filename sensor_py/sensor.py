import RPi.GPIO as GPIO
import time
import sys
import serial

#ピン設定
trig_pin = 15								#トリガーピン
echo_pin = 14								#エコーピン
speed_of_sound = 34370						#音速

distance = 0.0								#測定結果を格納する変数

#シリアル通信初期化
try:
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1, write_timeout=1)
except serial.SerialException as e:
	print(f"Serial connection failed: {e}")	#エラーのとき
	sys.exit(1)								#プログラム終了

#GPIOピン初期化
GPIO.setmode(GPIO.BCM)						#GPIO
GPIO.setwarnings(False)						#警告無効
GPIO.setup(trig_pin, GPIO.OUT)				#トリガーピン出力設定
GPIO.setup(echo_pin, GPIO.IN)				#エコーピン入力設定

time.sleep(2)								#初期化待機
print('now running...')

def get_distance():
	"""
	実際に距離を測定する関数
	返り値: 成功時は 測定距離 (cm) 
		        失敗時は -1
	"""
	
	#超音波パルスを送信
	GPIO.output(trig_pin, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(trig_pin, GPIO.LOW)
	
	#信号が戻るまで待つ(タイムアウトは20ms)
	start_time = time.monotonic()
	timeout = start_time + 0.02
	
	while not GPIO.input(echo_pin):
		if time.monotonic() > timeout:		#反射波が戻ってこなかったとき
			print("Echo pin never went HIGH")
			return -1
			
	t1 = time.monotonic()					#エコーピンがHIGHになった時点の時間
	
	#信号が戻るまでの時間を測る(タイムアウトは20ms)
	timeout = t1 + 0.02
	while GPIO.input(echo_pin):
		if time.monotonic() > timeout:		#HIGHが長すぎたとき
			print("Echo pin stayed HIGH too long")
			return - 1
			
	t2 = time.monotonic()					#エコーピンが再びHIGHになった時点の時間
	
	return (t2 - t1) * speed_of_sound / 2	#cm単位で距離を計算
	
try:
	while True:
		#測定結果の表示
		distance = get_distance()
		print("Distance: {:.1f} cm".format(distance))
		#シリアル通信で測定結果を送信する
		send_str = f"{distance:.2f}\n"
		ser.write(send_str.encode('utf-8'))
		time.sleep(0.1)						#データ送信の感覚調整
		ser.flush()							#送信バッファをフラッシュ
		time.sleep(4)						#次の測定まで4秒待機
		
except KeyboardInterrupt:					#Ctrl+Cで終了
	print("\nProgram interrupted by user")
	sys.exit(0)
		
except Exception as e:
	print(f"\nUnexpected error: {e}")		#その他異常終了
	sys.exit(1)

finally:
	#GPIOリセット
	GPIO.cleanup()
	#シリアル通信を終わらせる
	try:
		ser.close()
	except Exception as e:
		print(f"\nUnexpected error at loop {i}: {e}")
		print(f"Error while closing serial: {e}")
	sys.exit()
