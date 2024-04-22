from pymavlink import mavutil
import random
import time
import math

# Set the connection parameters (change accordingly)
connection_string = '/dev/ttyAMA0' # UART connection
baudrate = 57600   

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)


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

def send_telem(coords, phase):
    '''
    sends telemetry data to pixhawk from pi
    '''

    MAX_BANK_ANGLE = 45  #Maximum allowable bank angle in degrees
    #Convert maximum bank angle to radians for MAVLink parameter
    max_bank_angle_rad = MAX_BANK_ANGLE * (math.pi / 180) #Maximum allowable bank angle in radians

    altitude = altitude_handle(phase)
    # Send telemetry data to Pixhawk
    master.mav.mission_item_send(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, max_bank_angle_rad, 0, 0,
        coords['latitude'], coords['longitude'], altitude)

def receive_telem():
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
    if phase == 'SURVEILLANCE' or phase == 'END_MISSION': 
        return 45.72  
    if phase == 'DROP':
        #dunno what we want here
        return 25.908