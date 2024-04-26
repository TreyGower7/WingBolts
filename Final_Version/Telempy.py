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
    # Extract mode from the heartbeat message
    current_mode = msg.custom_mode

    print("Current Mode:", current_mode)
    # Check if current mode is "AUTO"
    if current_mode == 10:
        print("Mode is autopilot (AUTO)")
        return 'AUTO'
    else:
        print("Mode is not autopilot")
        return None
    
#****Tested and works*****
def send_telem(master, waypoints,phase):
    wp = mavwp.MAVWPLoader()   
    altitude = altitude_handle(phase)                                                 
    seq = 1
    frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    radius = 10
    N = len(waypoints)
    for i in range(N):                  
        wp.add(mavutil.mavlink.MAVLink_mission_item_message(master.target_system,
                    master.target_component,
                    seq,
                    frame,
                    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                    0, 0, 0, radius, 0, 0,
                    waypoints[i]['lat'],waypoints[i]['lon'], altitude))
        seq += 1                                                                       

    master.waypoint_clear_all_send()                                     
    master.waypoint_count_send(wp.count())                          

    for i in range(wp.count()):
        msg = master.recv_match(type=['MISSION_REQUEST'],blocking=True)             
        master.mav.send(wp.wp(msg.seq))                                                                      
        print(f'Sending waypoint {msg.seq}')  
        
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
        return 91.44
    if phase == 'SURVEILLANCE':
        return 60.96
    if phase == 'DROP':
        #dunno what we want here
        return 25.908
    if phase == 'PRE_MISSION': 
        return 91.44 
