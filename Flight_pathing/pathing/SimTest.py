import sys
sys.path.append(r"C:\Users\gower\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages")
from pymavlink import mavutil
import random
import time
import math


# Set the connection parameters (change accordingly)
connection_string = 'udp:127.0.0.1:14550' # sim connection

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string)


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

def Search_zigzag():
    '''
    Search phase for targets
    '''
    alt = 76.2 #meters
    phase = 'surveillance'

    waypoints = [
    {"lat":   30.323221, "lon":  -97.602798},
    {"lat": 30.323180, "lon": -97.601598},
    {"lat":   30.323715, "lon": -97.603007},
    {"lat": 30.324627, "lon": -97.602312},
    {"lat": 30.325696, "lon": -97.603918},
    ]   
    
    #populate waypoints for initial search phase
    for i in range(len(waypoints)):
        coords = {'latitude': waypoints[i]['lat'], 'longitude': waypoints[i]['lon']}
        send_telem(coords, phase)
        print(f"Sending waypoint {i+1}: ({waypoints[i]['lat']}, {waypoints[i]['lon']})")
    #Set vehicle mode to Auto (numerical value for Auto mode is 4)
    print("Setting vehicle mode to Auto...")
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        4  # Numerical value for Auto mode
    )

    print("Waypoints sent to Mission Planner.")
        
    return waypoints


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

    MAX_BANK_ANGLE = 30  #Maximum allowable bank angle in degrees
    #Convert maximum bank angle to radians for MAVLink parameter
    max_bank_angle_rad = MAX_BANK_ANGLE * (math.pi / 180) #Maximum allowable bank angle in radians

    altitude = altitude_handle(phase)
    # Send telemetry data to Pixhawk
    msg = master.mav.mission_item_send(
        0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, max_bank_angle_rad, 0, 0,
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
                break
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
    

    if distance < 0.001:
        print(f"Reached waypoint: {waypoints[0][0]}, {waypoints[0][1]}")
        waypoints.pop(0)  # Remove the reached waypoint
    
    return waypoints


def main():
    ''' Main Func '''
    #surveillance phase initially true to start
    phase_search = True
    phase_surveillance = True

    #Populate Coordinates for Search phase
    waypoints = Search_zigzag()
    while phase_search == True:
        #constantly updating waypoints
        print("Checking Waypoint Progress")
        waypoints = haversine_check(waypoints)

        #***Check target recognition for waypoints of objects***

        #once zig zag is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            phase_search = False
             #first random point
            coords = get_telem()
            send_telem(coords, 'surveillance')
            break
        
    while phase_surveillance == True:
        haversine_check(coords)
        coords = get_telem()
        send_telem(coords, 'surveillance')

        time.sleep(5)  #Adjust as needed for the update frequency

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()
