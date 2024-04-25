from pymavlink import mavutil, mavwp
import random
import time
import math


def check_AUTO(master):
    '''
    Checks if the mode is in autopilot
    '''
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    current_mode = mavutil.mode_string_v10(msg)
            
    # Check if current mode is "AUTO"
    if current_mode == "AUTO":
        print("Mode is autopilot (AUTO)")
        return 'AUTO'
    else:
        print("Mode is not autopilot")
        return None
    
#****Tested and works*****
def send_telem(master, waypoints,phase):
    altitude = altitude_handle(phase)                                                 
       # Clear existing waypoints
    master.mav.mission_clear_all_send(
        master.target_system, master.target_component)
    time.sleep(1)

    # Send new waypoints
    seq = 0
    for i in range(len(waypoints)):
        master.mav.mission_item_send(
            master.target_system, master.target_component,
            seq,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0, 0, 0, 0,
            waypoints[i]['lat'], waypoints[i]['lon'], altitude)
        seq += 1
        time.sleep(0.2)  # Add a small delay to ensure waypoints are sent sequentially 
    while True:
        msg = master.recv_match(type=['MISSION_ACK'], blocking=True)
        if msg:
            print("Waypoints updated successfully")
            break
#****Tested and works*****
def receive_telem(master):
    '''
    receives telemetry data from pixhawk to pi
    '''
    #message
    msg = master.recv_match(type=['GLOBAL_POSITION_INT'],blocking=True)             
    # Check if message is not None
    if msg:
        print("Global Position: Lat={}, Lon={}, Alt={}".format(msg.lat, msg.lon, msg.alt))        
        # Sleep for a short duration to avoid busy-waiting
        time.sleep(0.1)
        
        return msg
            
#*******Tested and Working*******  
def altitude_handle(phase):
    '''
    handles the altitude inputs to the plane
    '''
    #Altitudes are in meters
    if phase == 'SEARCH':
        return 76.2 
    if phase == 'DROP':
        #dunno what we want here
        return 25.908
    if phase == 'END_MISSION': 
        return 45.72 