from pymavlink import mavutil
import random
import time

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

def check_waypoint(waypoints):
    '''
    Calulates how close plane is to waypoint
    '''
    #get current position
    msg = receive_telem()
    current_lat = msg.lat
    current_lon = msg.lon

    if (abs(current_lat - waypoints[0][0]) < 0.0001 and 
        abs(current_lon - waypoints[0][1]) < 0.0001):
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
        waypoints = check_waypoint(waypoints)

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
        check_waypoint(coords)
        coords = get_telem()
        send_telem(coords, 'surveillance')

        time.sleep(5)  #Adjust as needed for the update frequency

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()
