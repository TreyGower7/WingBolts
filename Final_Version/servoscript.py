from gpiozero import Servo
from time import sleep

from gpiozero import Servo
from time import sleep

# Define servo and PWM values
servo = Servo(26)
neutral_pwm = 0   # Neutral position
adp1_pwm = -1     # ADP1 position
adp2_pwm = 1      # ADP2 position

try:
    while True:
        servo.value = neutral_pwm
        print("Moved to Neutral position")
        sleep(2)

        servo.value = adp1_pwm
        print("Moved to ADP1 position")
        sleep(2)

        servo.value = adp2_pwm
        print("Moved to ADP2 position")
        sleep(2)

except KeyboardInterrupt:
    servo.detach()

