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
    coords = {'lat': lat, 'lon': lon}
    return coords

def Search_zigzag():
    '''
    Search phase for targets
    '''
    phase = 'search'
    altitude = altitude_handle(phase)


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
        print(f"Sending waypoint {i+1}: ({waypoints[i]['lat']}, {waypoints[i]['lon']}, {altitude})")

    print("Waypoints sent to Mission Planner.")
        
    return waypoints


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
    print(f"Sending waypoint: ({ coords['latitude']}, {coords['longitude']}, {altitude})")


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
    
def check_AUTO():
    '''
    Checks if the mode is in autopilot
    '''
    # Wait for response
    while True:
        msg = master.recv_match(type='HEARTBEAT', blocking=True)
        if msg:
            current_mode = mavutil.mode_string_v10(msg)
            break
    
    # Check if current mode is "AUTO"
    if current_mode == "AUTO":
        print("Mode is autopilot (AUTO)")
        return 'AUTO'
    else:
        print("Mode is not autopilot")
        return None

#*******Tested and Working*******  
def altitude_handle(phase):
    '''
    handles the altitude inputs to the plane
    '''
    #Altitudes are in meters
    if phase == 'search':
        return 91.44
    if phase == 'surveillance':
        return 45.72  

#*******Tested and Working*******
def haversine_check(waypoints, use, ref_waypoint):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers

    if use == 'Update_waypoints':
        #get current position
        msg = receive_telem()
        current_lat = msg.lat
        current_lon = msg.lon
        waypoint_lat = waypoints[0]['lat']
        waypoint_lon = waypoints[0]['lon']
    if use == 'Distance':
        #only requires one point for input
        current_lat = ref_waypoint['lat']
        current_lon = ref_waypoint['lon']
        waypoint_lat = waypoints['lat']
        waypoint_lon = waypoints['lon']
       
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

    if use == 'Update_waypoints':
        if distance < 0.003048: #10 feet
            print(f"Reached waypoint: {waypoints[0][0]}, {waypoints[0][1]}")
            waypoints.pop(0)  # Remove the reached waypoint
        else:
            print(f'Distance from waypoint: {distance}')
        return waypoints
    
    if use == 'Distance':
        return distance

#*******Tested and Working*******
def sort_obj_waypoints(reference_waypoint, Obj_waypoints): 
    '''
    sort the waypoints of the objects from closest to farthest
    '''
    
    #Calculate distances and store them along with object waypoints
    obj_distances = [(waypoint, haversine_check(waypoint, 'Distance', reference_waypoint)) for waypoint in Obj_waypoints]
    
    #Sort the object waypoints based on distances
    sorted_obj = [waypoint for waypoint, _ in sorted(obj_distances, key=lambda x: x[1])]
    
    return sorted_obj

def drop_line():
    '''
    calculates optimal drop line for targets
    '''


def main():
    ''' Main Func '''
    phase = None
    mode = None
    Obj_waypoints = []
    #Ensures we manually set the mode to AUTO
    while mode is None:
        mode = check_AUTO()
        if mode == 'AUTO':
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            phase = 'search'
            break

    #saves last waypoint for sorting alg
    last_waypoint= waypoints[-1]

    while phase == 'search':
        #Auto Pilot Check
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(.5)
                mode = check_AUTO()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break
        #constantly updating waypoints
        print("Checking Waypoint Progress")
        waypoints = haversine_check(waypoints, 'Update_waypoints', None)
        time.sleep(.2)  #Adjust as needed for the update frequency
        
        #*************
        #***Check target recognition for waypoints of objects***
        #Obj_waypoints.append(object_coords()) Something like this
        #returns: {'lat': lat, 'lon': lon} of object
        #*************

        #once zig zag is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            phase = 'surveillance'
                    #Insert waypoints of objects 
            #****Remember to remove for loop****
            for i in range(6): #generates 6 random objects
                Obj_waypoints.append(get_obj_coords())

            #Sorting Algorithmn
            sort_obj_waypoints(last_waypoint, Obj_waypoints)
            send_telem(Obj_waypoints, phase)
            break
    

    while phase == 'surveillance':
        #Auto Pilot Check
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(.5)
                mode = check_AUTO()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break

        #constantly updating waypoints
        print("Checking Waypoint Progress")
        Obj_waypoints = haversine_check(Obj_waypoints,'Update_waypoints', None)
        time.sleep(.2)  #Adjust as needed for the update frequency

        #once zig zag is complete we go to next phase
        if len(Obj_waypoints) == 0:
            print("All Object Waypoints Reached")
            phase = 'drop'
            break
        
    while phase == 'drop':


        time.sleep(.2)  #Adjust as needed for the update frequency

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()
