from pymavlink import mavutil
import random
import time

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


def get_telem():
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
    altitude = altitude_handle(phase)
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
            
        
                        
        # Sleep for a short duration to avoid busy-waiting
        time.sleep(0.1)
        
        return msg
    
def altitude_handle(phase):
    '''
    handles the altitude inputs to the plane
    '''
    #Altitudes are in meters
    if phase == 'search':
        return 91.44
    if phase == 'surveillance':
        return 45.72  
    
