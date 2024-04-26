from gpiozero import Servo
from time import sleep

# Define servo and PWM values
servo = Servo(26)
neutral_pulse_width = 1556  # Neutral pulse width in microseconds
adp1_pulse_width = 1193     # ADP1 pulse width in microseconds
adp2_pulse_width = 2000     # ADP2 pulse width in microseconds

# Define function to convert pulse width to angle
def pulse_width_to_angle(pulse_width):
    # Assuming a typical servo range of 1000 to 2000 microseconds
    return (pulse_width - 1000) / (2000 - 1000) * 180

try:
    while True:
        servo.value = pulse_width_to_angle(neutral_pulse_width)
        print("Moved to Neutral position")
        sleep(2)

        servo.value = pulse_width_to_angle(adp1_pulse_width)
        print("Moved to ADP1 position")
        sleep(2)

        servo.value = pulse_width_to_angle(adp2_pulse_width)
        print("Moved to ADP2 position")
        sleep(2)

except KeyboardInterrupt:
    servo.detach()


