import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo
servo_pin = 26

# Set PWM parameters
frequency = 50  # Hz
neutral_duty_cycle = 7.5  # Duty cycle for neutral position (in %)
adp1_duty_cycle = 4.5     # Duty cycle for ADP1 position (in %)
adp2_duty_cycle = 10.0    # Duty cycle for ADP2 position (in %)

# Calculate duty cycle in microseconds
def us_to_duty_cycle(us):
    return (us / 1000.0) * frequency

# Initialize servo PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, frequency)
pwm.start(neutral_duty_cycle)

try:
    while True:
        # Move to Neutral position
        pwm.ChangeDutyCycle(neutral_duty_cycle)
        time.sleep(2)
        
        # Move to ADP1 position
        pwm.ChangeDutyCycle(adp1_duty_cycle)
        time.sleep(2)
        
        # Move to ADP2 position
        pwm.ChangeDutyCycle(adp2_duty_cycle)
        time.sleep(2)

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    pwm.stop()
    GPIO.cleanup()
