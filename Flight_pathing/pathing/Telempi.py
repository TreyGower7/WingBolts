from RandLatlon import random_coords
from pymavlink import mavutil
import time
"""
Updating pixhawk from our ML model
"""


#Connect Pi to Pixhawk

'''
connect = mavutil.mavlink_connection('udpin:localhost:14550')

# Waits for first heartbeat **only need loop for viewing purposes**
while not connect.wait_heartbeat():
    print('Waiting for Connection')
    time.sleep(1)

print(f'Heartbeat from system: {connect.target_system()}, component: {connect.target_component()} ')
'''
__author__ = "Trey Gower"

def get_telem():
    '''
    Gets Telemetry data from Pixhawk
    '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    coords = random_coords(domain)
    return coords
"""Need to test with pi and pixhawk
def send_telem(coords):
    '''
    #sends telemetry data to pixhawk from pi
    '''
     # Send telemetry data to Pixhawk
    msg = mavutil.mavlink.MAVLink_mission_item_message(
        0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0,
        coords['latitude'], coords['longitude'], coords['altitude'])
    connect.mav.send(msg)

def recieve_telem():
    '''
    #recieves telemetry data to pixhawk from pi
    '''
    #Receive a message
    msg = connect.recv_match()
        
        #Check if message is not None
    if msg:
        #Print the message
        print(msg)
    return msg
    
 def altitude_handle():
    '''
    #handles the altitude inputs to the plane
    '''
"""

def main():
    ''' Main Func '''
    coords = get_telem()
if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()