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
    

def haversine_check(waypoints):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers
    #get current position
    msg = receive_telem()
    current_lat = msg.lat
    current_lon = msg.lon
    waypoint_lat = waypoints[0]['lat']
    waypoint_lon = waypoints[0]['lon']

    # Convert latitude and longitude from degrees to radians
    current_lat = math.radians(current_lat)
    current_lon = math.radians(current_lon)
    waypoint_lat = math.radians(waypoint_lat)
    waypoint_lon = math.radians(waypoint_lon)

    # Calculate the differences in latitude and longitude
    dlat = waypoint_lat - current_lat
    dlon = waypoint_lon - current_lon

    # Apply the Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(current_lat) * math.cos(waypoint_lat) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    if distance < 0.003048: #10 feet
        print(f"Reached waypoint: {waypoints[0][0]}, {waypoints[0][1]}")
        waypoints.pop(0)  # Remove the reached waypoint
    else:
        print(f'Distance from waypoint: {distance}')
    
    return waypoints