# Fly Off Commands
### Scripts (Ensure All of These Are Loaded on The Pi):
`Main_Loop_Final.py`  
`Object_loc.py`
`Phases.py`  
`Sorting_Distance.py`  
`Telempy.py`  
`servoscript.py` 
`tflite_webcam_bboxes.py`  
`trajectory.py`  

#### Run these commands on the raspberry pi pre-flight:
- 1. Run the ML model
  - `python3 tflite_webcam_bboxes.py --modeldir=custom_model_lite`
- 2. In a seperate terminal run `Main_Loop_Final.py`:
  - `sudo python3 Main_Loop_Final.py --master=/dev/tty/AMA0`

***NOTE: Ensure the servoscript is tested before proceeding with Main_Loop_Final.py (If the servo is drawing too much current it will crash the Pi)***

# Testing 
## Ground Testing 
### Scripts:
`Groundtest.py`  
`mavproxy.py`
#### Run these commands on the raspberry pi:
First to check outputs:
`sudo mavproxy.py --master=/dev/tty/AMA0`  
Second to send waypoints to walk to at ARCA (runs in a loop until 
all waypoints are reached):
`sudo python3 Groundtest.py --master=/dev/tty/AMA0`

## Air Testing (Pre-Flight)
### Scripts:
`04-26TDV.py`  
`mavproxy.py`
#### Run this command on the raspberry pi Pre-Flight: 
Send waypoints to fly the plane to at ARCA (runs in a loop until 
all waypoints are reached):

`sudo python3 04-26TDV.py --master=/dev/tty/AMA0`

***NOTE: Once the script is ran, takeoff manually, and then ensure 
the plane is set to AUTO mode (script will not run until it is)***
