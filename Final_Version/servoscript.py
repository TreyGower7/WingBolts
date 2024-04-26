from gpiozero import Servo
from time import sleep

def servo_activate():
   servo = Servo(26)
   try:
      #while True:
      servo.min(1193)
      print('Servo Min')
      sleep(0.5)
      servo.mid(1556)
      print('Servo Mid')
      sleep(0.5)
      print('Servo Max')
      servo.max()
      sleep(0.5)
   except KeyboardInterrupt:
      print("Program stopped")
