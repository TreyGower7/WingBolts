from pymavlink import mavutil, mavwp
import random
import time
import math


# Set the connection parameters (change accordingly)
connection_string = '/dev/ttyAMA0'
baudrate = 57600

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
    phase = 'SEARCH'
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
    
def check_AUTO():
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

#*******Tested and Working*******
def haversine_check(waypoints, use, ref_waypoint):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers

    if use == 'Update_waypoints' or use == 'Drop':
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
    
    if use == 'DROP':
        if distance <= 0.0009144: #3 feet
            waypoints.pop(0)  # Remove the reached waypoint
            return 'DROP_SIGNAL', waypoints
        else:
            return 'WAIT', None

def haversine_high_frequency(drop_points):
    '''
    High frequency update of plane location for the most accurate dropping position
    '''
    while True:
        Signal, drop_points = haversine_check(drop_points, 'DROP', None)
        if Signal == 'DROP_SIGNAL':
            #***Drop Payload by calling servo actuating function here***
            break
    return drop_points
    
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

def predrop_phase(refinedobj_waypoints, phase):
    '''
    Sets the plane up for dropping the payload
    '''
    distressed_waypoints = []
    happy_waypoints = []

    #fly out to random point to prepare for payload drop
    reset_waypoint = {'lat': 30.323246847038178, 'lon': -97.60228430856947}
    send_telem(reset_waypoint, phase)
    print(f"Sending waypoint: ({reset_waypoint[i]['lat']}, {reset_waypoint[i]['lon']})")

    #Sort and send distressed targets
    #****Write these to a file to be saved***** 
    for i in range(len(refinedobj_waypoints)):
        if refinedobj_waypoints[i]['state'] == 'distressed':
            distressed_waypoints.append(refinedobj_waypoints[i])
        else:
            happy_waypoints.append(refinedobj_waypoints[i])

     #***Calculate drop points here in a loop and store them based on distressed_waypoints***
    #first drop point based on reset point, second drop point based on first object waypoint...
    drop_points = {'lat': 0, 'lon': 0}

    #Sort by distance
    drop_points = sort_obj_waypoints(reset_waypoint, drop_points)
    #Send sorted drop_point for target coords
    for i in range(len(drop_points)):
        #****Need to Add Loitering****
        coords = {'latitude': drop_points[i]['lat'], 'longitude': drop_points[i]['lon']}
        send_telem(coords, phase)
        print(f"Sending waypoint {i+1}: ({drop_points[i]['lat']}, {drop_points[i]['lon']})")
    
    return drop_points


def write_data():
    '''
    writes target locations, medical payload drop point, 
    time first detected to a data.txt file
    '''

def main():
    ''' Main Func '''
    phase = None
    mode = None
    Obj_waypoints = []
    #Ensures we manually set the mode to AUTO
    while mode is None:
        mode = check_AUTO()
        print('Waiting on Autopilot Mode')
        if mode == 'AUTO':
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            phase = 'SEARCH'
            break

    #saves last waypoint for sorting alg
    last_waypoint= waypoints[-1]

    while phase == 'SEARCH':
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
        #*************
        #***Check target recognition for waypoints of objects***
        #Obj_waypoints.append(get_object_coords()) Something like this
        #returns: {'lat': lat, 'lon': lon, 'state': state} of object and stress state too
        #*************
        time.sleep(.2)  #Adjust as needed for the update frequency

        #once zig zag is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            phase = 'SURVEILLANCE'
                    #Insert waypoints of objects 
            #****Remember to remove for loop****
            for i in range(6): #generates 6 random objects
                Obj_waypoints.append(get_obj_coords())

            #Sorting Algorithmn
            Obj_waypoints = sort_obj_waypoints(last_waypoint, Obj_waypoints)
            #Send coordinates to pixhawk
            for i in range(len(Obj_waypoints)):
                #****Need to Add Loitering****
                coords = {'latitude': Obj_waypoints[i]['lat'], 'longitude': Obj_waypoints[i]['lon']}
                send_telem(coords, phase)
                print(f"Sending waypoint {i+1}: ({Obj_waypoints[i]['lat']}, {Obj_waypoints[i]['lon']})")
            break
    
    while phase == 'SURVEILLANCE':
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
        
        #*************
        #***Check target recognition for refined waypoints and stress state of objects during loiter***
        #refinedobj_waypoints.append(get_object_coords()) Something like this
        #returns: {'lat': lat, 'lon': lon, 'state': state} of object and stress state too
        #*************

        #constantly updating waypoints
        print("Checking Waypoint Progress")
        Obj_waypoints = haversine_check(Obj_waypoints,'Update_waypoints', None)
        time.sleep(.2)  #Adjust as needed for the update frequency

        #once all objects are checked we go to next phase
        if len(Obj_waypoints) == 0:
            print("All Object Waypoints Reached")
            phase = 'DROP'
            break
    
    #Set the plane up for payload drop
    drop_points = predrop_phase(refinedobj_waypoints, phase)

    while phase == 'DROP':
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
        print("Checking For Payload Drop")
        drop_points = haversine_high_frequency(drop_points)

        #once payload are dropped we go to mission end
        if len(drop_points) == 0:
            print("All Payloads Dropped To Targets")
            phase = 'END_MISSION'
            break
        

        time.sleep(.2)  #Adjust as needed for the update frequency

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()
