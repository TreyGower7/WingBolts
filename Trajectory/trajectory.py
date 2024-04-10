import time
from pymavlink import mavutil
import numpy as np
import math
import random

connection_string = '/dev/ttyUSB0'  # or '/dev/ttyAMA0' for UART connection
baudrate = 115200  # or whatever baudrate your connection uses

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

def get_telem():
    '''
    Gets Telemetry data from Pixhawk
    '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    coords = random_coords(domain)
    return coords

def send_telem(coords):
    '''
    sends telemetry data to pixhawk from pi
    '''
    altitude = altitude_handle('surveillance')
    # Send telemetry data to Pixhawk
    msg = master.mav.mission_item_send(
        0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0,
        coords['latitude'], coords['longitude'], altitude)
    master.mav.send(msg)

def receive_telem():
    '''
    receives telemetry data from pixhawk to pi
    '''
    # Receive messages in a loop
    while True:
        # Wait for a message
        msg = master.recv_match()
        
        # Check if message is not None
        if msg:
            # Process messages of interest
            if msg.get_type() == 'GLOBAL_POSITION_INT':
                # Example: Print latitude, longitude, and altitude
                print("Global Position: Lat={}, Lon={}, Alt={}".format(msg.lat, msg.lon, msg.alt))
            elif msg.get_type() == 'STATUSTEXT':
                # Example: Print status text messages
                print("Status Text: {}".format(msg.text))
            # Add more conditions to handle other message types as needed
            # elif msg.get_type() == 'SOME_OTHER_MESSAGE_TYPE':
            #    ...
            
            # Example: Check if message is a heartbeat
            if msg.get_type() == 'HEARTBEAT':
                print("Received heartbeat from system {} component {}".format(msg.get_srcSystem(), msg.get_srcComponent()))
                
        # Add other logic here if needed
        
        # Sleep for a short duration to avoid busy-waiting
        time.sleep(0.1)
    
def altitude_handle(phase):
    '''
    handles the altitude inputs to the plane
    '''
    #Altitudes are in meters
    if phase == 'search':
        return 76.2
    if phase == 'surveillance':
        return 45.72  

def projectile_range(v_x, v_y, H):
    """
    Using random numbers for the variables as placeholders until we find out how to get the data from Pixhawk
    This is a SUPER rough code straight from the research paper
    """

    # these are constant parameters that should be stored beforehand
    rho = 1.225 # kg/m density of air
    Cd = 0 # drag coefficient, proportional to airspeed?

    # A does not include the grid fins yet
    A = 0.0157 # surface area of the payload in m^2 (2 in diameter, 3 in length)
    m = 0.181 # payload mass in kg (0.4 lb)

    q = 0.5*rho*Cd*A
    dt = 0.02 # time interval
    N = 3000 # max iterations

    iters = 0
    x = 0
    y = 0
    t = 0
    while (iters < N):

        if (y >= H):
            R = x
            break

        a_x = -(q/m)*v_x**2
        a_y = 9.81 - (q/m)*v_y**2

        v_x += a_x*dt
        v_y += a_y*dt

        x += v_x*dt + 0.5*a_x*dt**2
        y += v_y*dt + 0.5*a_y*dt**2

        t += dt # total time, don't know what this is useful for?
    

        iters += 1

    return(R,t)

def release_point(target_long, target_lat, R, current_long, current_lat):
    z = (target_long - current_long)/(target_lat - current_lat)
    theta = math.atan(z)
    RP_lat = target_lat - R*math.sin(theta)
    RP_long = target_long - R*math.cos(theta)
    return(RP_lat, RP_long)


def geo_to_cartesian(latitude, longitude):
    # have to double check that this is how you calculate it
    r = 6371
    lat = math.radians(latitude)
    lon = math.radians(longitude)
    x = r*math.cos(lat)*math.cos(lon)
    y = r*math.cos(lat)*math.sin(lon)
    return(x,y)


if __name__ == "__main__":
    altitude = 45.72 # surveillance phase
    print(projectile_range())



