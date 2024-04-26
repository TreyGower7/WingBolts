import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
servo_pin = 26

# Set the PWM parameters
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms period)

# Define PWM values for Neutral, ADP1, and ADP2
neutral_pwm = 1556  # Neutral pulse width in microseconds
adp1_pwm = 1193     # ADP1 pulse width in microseconds
adp2_pwm = 2000     # ADP2 pulse width in microseconds

# Function to convert microseconds to duty cycle
def us_to_dc(us):
    return us / 20.0  # 20 ms is the period

try:
    pwm.start(us_to_dc(neutral_pwm))  # Set to Neutral position initially
    time.sleep(1)  # Wait for servo to move to the Neutral position

    while True:
        pwm.ChangeDutyCycle(us_to_dc(neutral_pwm))  # Move to Neutral
        time.sleep(2)  # Wait for 2 seconds
        pwm.ChangeDutyCycle(us_to_dc(adp1_pwm))  # Move to ADP1
        time.sleep(2)  # Wait for 2 seconds
        pwm.ChangeDutyCycle(us_to_dc(adp2_pwm))  # Move to ADP2
        time.sleep(2)  # Wait for 2 seconds

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
