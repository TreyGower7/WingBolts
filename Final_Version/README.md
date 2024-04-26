# Ground Testing 
## Scripts:
`Groundtest.py`  
`mavproxy.py`
### Run these commands on the raspberry pi:
First to check outputs:
`sudo mavproxy.py --master=/dev/tty/AMA0`  
Second to send waypoints to walk to at ARCA (runs in a loop until 
all waypoints are reached):
`sudo python3 Groundtest.py --master=/dev/tty/AMA0`

# Air Testing (Pre-Flight)
## Scripts:
`04-26TDV.py`  
`mavproxy.py`
### Run this commands on the raspberry pi Pre-Flight: 
Send waypoints to fly the plane to at ARCA (runs in a loop until 
all waypoints are reached):
`sudo python3 04-26TDV.py --master=/dev/tty/AMA0`

***NOTE: Once the script is ran takeoff manually and then ensure 
the plane is set to AUTO mode (script will not run until it is)***
