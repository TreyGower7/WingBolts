from pymavlink import mavutil, mavwp
import random
import time
import math

def random_coords(domain):
    """
    *********************
    ** Only Using For Sims **
    *********************
    Generate random latitude and longitude within a specified domain.

    Args:
    Tuple (min_lat, max_lat, min_lon, max_lon)

    Returns:
    Tuple (latitude, longitude)
    """
    min_lat, max_lat, min_lon, max_lon = domain
    lat = random.uniform(min_lat, max_lat)
    lon = random.uniform(min_lon, max_lon)
    coords = {'latitude': lat, 'longitude': lon}
    return coords


def get_obj_coords():
    '''
    Gets Telemetry data from Pixhawk
    '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    coords = random_coords(domain)
    return coords

#****Tested and works*****
def send_telem(master, waypoints,phase):
    wp = mavwp.MAVWPLoader()   
    altitude = altitude_handle(phase)                                                 
    seq = 1
    frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    #radius = 10
    N = len(waypoints)
    for i in range(N):    
        master.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, master.target_system,
                        master.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, int(0b110111111000), 
                        int(waypoints[i]['lat'] * 10 ** 7), int(waypoints[i]['lon'] * 10 ** 7), altitude, 0, 0, 0, 0, 0, 0, 0, 0)) 
            
        msg = master.recv_match(
        type='LOCAL_POSITION_NED', blocking=True)
        print(msg)        
        # wp.add(mavutil.mavlink.MAVLink_mission_item_message(master.target_system,
        #             master.target_component,
        #             seq,
        #             frame,
        #             mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        #             0, 0, 0, radius, 0, 0,
        #             waypoints[i]['lat'],waypoints[i]['lon'], altitude))
        seq += 1                                                                       

    # master.waypoint_clear_all_send()                                     
    # master.waypoint_count_send(wp.count())                          

    # for i in range(wp.count()):
    #     msg = master.recv_match(type=['MISSION_REQUEST'],blocking=True)             
    #     master.mav.send(wp.wp(msg.seq))                                                                      
    #     print(f'Sending waypoint {msg.seq}')    

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