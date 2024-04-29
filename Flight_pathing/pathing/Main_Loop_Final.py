#from Sorting_Distance import haversine_check, haversine_high_frequency
#from Phases import Search_zigzag, predrop_phase
#from Telempy import send_telem, check_AUTO, receive_telem
import time
from pymavlink import mavutil, mavwp
import json
from Object_loc import Obj_main
from servoscript import servo_activate
import math



"""
Main script for connecting to pixhawk,
sending/recieving coordinates from raspberry pi to pixhawk 
and updating waypoints based on ML
"""

__author__ = "Trey Gower"

connection_string = '/dev/ttyAMA0' #Pin connectors for Pi
#connection_string = '/dev/ttys039' #virtual connection for testing

baudrate = 57600  

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)
master.wait_heartbeat()
print(f"Heartbeat from system ({master.target_system}, {master.target_component})")


def get_connection():
    return master

def Search_zigzag():
    waypoints = [
        {"lat":   30.322588, "lon":  -97.602679},
        {"lat": 30.322291634213112, "lon": -97.6018262396288},
        {"lat":  30.323143653772693, "lon": -97.60142927270336},
        {"lat": 30.325269418344888, "lon": -97.60358765983898},
        {"lat": 30.32556423886435, "lon": -97.60242970541643},
        {"lat": 30.323148122665625, "lon": -97.60268795424491},
    ]   
    return waypoints


def predrop_phase(obj_waypoints):
    '''
    Sets the plane up for dropping the payload
    '''
    sad_waypoints = []
    happy_waypoints = []

    #fly out to random point to prepare for payload drop
    reset_waypoint = {'lat': 30.322416459788805, 'lon': -97.60161890138745}

    #Sort and send distressed targets

    #****Write these to a file to be saved***** 
    for i in range(len(obj_waypoints)):
        if obj_waypoints[i]['state'] == 'sad':
            sad_waypoints.append(obj_waypoints[i])
        else:
            happy_waypoints.append(obj_waypoints[i])

     #***Calculate drop points here in a loop and store them based on distressed_waypoints***
    #first drop point based on reset point, second drop point based on first object waypoint...
    #List of dictionaries format
    #Starting from the reset_waypoint
    drop_points = [reset_waypoint]
    current_lon = reset_waypoint['lon']
    current_lat = reset_waypoint['lat']
    for i in range(len(sad_waypoints)):
        RP = traj_main(current_lon, current_lat, sad_waypoints[i]['lon'], sad_waypoints[i]['lat'])
        drop_points.append(RP)
        current_lon = RP['lon']
        current_lat = RP['lat'] 

    
    return drop_points

#*******Tested and Working*******
def haversine_check(waypoints, use, ref_waypoint):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers

    if use == 'Update_waypoints' or use == 'DROP':
        #get current position
        msg = receive_telem()
        current_lat = msg.lat/(10^7)
        current_lon = msg.lon/(10^7)
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
        if distance < 0.006096: #20 feet
            print(f"Reached waypoint: {waypoints[0][0]}, {waypoints[0][1]}")
            waypoints.pop(0)  # Remove the reached waypoint
        else:
            print(f'Distance from waypoint: {distance}')
        return waypoints
    if use == 'Distance':
        return distance
    
    if use == 'DROP':
        if distance <= 0.003048: #10 feet
            waypoints.pop(0)  # Remove the reached waypoint
            return 'DROP_SIGNAL', waypoints
        else:
            return 'WAIT', None

def haversine_high_frequency(drop_points, adp):
    '''
    High frequency update of plane location for the most accurate dropping position
    '''
    #value for which adp to activate
    while True:
        Signal, drop_points = haversine_check(drop_points, 'DROP', None)
        if Signal == 'DROP_SIGNAL':
            servo_activate(adp)
            break
    return drop_points

#*******Tested and Working*******
def sort_obj_waypoints(reference_waypoint, Obj_waypoints): 
    '''
    sort the waypoints of the objects from closest to farthest
    '''
    
    #Calculate distances and store them along with object waypoints
    obj_distances = [(waypoint, haversine_check(master,waypoint, 'Distance', reference_waypoint)) for waypoint in Obj_waypoints]
    
    #Sort the object waypoints based on distances
    sorted_obj = [waypoint for waypoint, _ in sorted(obj_distances, key=lambda x: x[1])]
    
    return sorted_obj

    
def check_AUTO():
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
def send_telem(waypoints,phase):
    wp = mavwp.MAVWPLoader()   
    altitude = altitude_handle(phase)                                                 
    seq = 1
    frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    radius = 5 #
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
    if phase == 'SURVEILLANCE':
        return 60.96
    if phase == 'DROP':
        return 25.908
    if phase == 'PRE_MISSION': 
        return 91.44 

    
def main():
    ''' Main Func '''
    phase = 'PRE_MISSION'
    mode = None
    Obj_waypoints = []

    distance = 0
    firstWaypoints = [
            {"lat":  30.322625102951214, "lon": -97.60248728111718},
            {"lat": 30.32295838950817, "lon": -97.60131930392731},
            {"lat": 30.325349687298175, "lon": -97.6024100594848},
            {"lat": 30.324727584029873, "lon": -97.60292879852376},
            {"lat": 30.323560701045245, "lon": -97.60261830821472}
    ]
    firstWaypoints_copy = firstWaypoints.copy()

    for i in range(len(firstWaypoints)):
        distance += haversine_check(firstWaypoints[i-1], 'Distance', firstWaypoints[i])
    #Distance of one loop # after 3 nautical miles: 1 meter = 0.000539957 miles
    nautMiles = distance * 0.539957
    total_naut_miles = 0
    numofloops = 0
    while total_naut_miles <= 3:
        total_naut_miles += nautMiles
        numofloops += 1;
        print(total_naut_miles)

    for i in range(numofloops-1):
        #For the Next loop
        firstWaypoints.extend(firstWaypoints_copy)
    print(len(firstWaypoints))

    #fly three nautical miles
    
    send_telem(firstWaypoints, phase)
    
    #Ensures we manually set the mode to AUTO
    while mode is None:
        mode = check_AUTO()
        if mode == 'AUTO':
            break
        else:
            print('Waiting on Autopilot Mode')

    while phase == 'PRE_MISSION':
        #Auto Pilot Check
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(1)
                mode = check_AUTO()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break
        #constantly updating waypoints
        print("Checking Waypoint Progress")
        firstWaypoints = haversine_check(firstWaypoints, 'Update_waypoints', None)        

        time.sleep(.5)  #Adjust as needed for the update frequency

        if len(firstWaypoints) == 0:
            print("All waypoints reached")
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            #populate waypoints for initial search phase
            phase = 'SEARCH'
            send_telem(waypoints, phase)
            break


    while phase == 'SEARCH':
        #Auto Pilot Check
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(1)
                mode = check_AUTO()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break

        #constantly updating waypoints
        print("Checking Waypoint Progress")
        waypoints = haversine_check(waypoints, 'Update_waypoints', None)        
    
        time.sleep(.5)  #Adjust as needed for the update frequency

        #once search is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            phase = 'SURVEILLANCE'
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            #populate waypoints for initial search phase
            send_telem(waypoints, phase)
            break

    #Another phase that changes altitude
    while phase == 'SURVEILLANCE':
        #Auto Pilot Check
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(1)
                mode = check_AUTO()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break
                
        #constantly updating waypoints
        print("Checking Waypoint Progress")
        waypoints = haversine_check(waypoints, 'Update_waypoints', None)        

        time.sleep(.5)  #Adjust as needed for the update frequency

        #once search is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            phase = 'DROP'
            break
        
    #Convert Bounding Boxes to Locations
    Obj_main()
    #Get Waypoints from json file predrop setup and send to pixhawk
    with open('Final_Version/target_coords.json', 'r') as f:
        Obj_waypoints = json.loads(f)

    #Set the plane up for payload drop

    drop_points = predrop_phase(Obj_waypoints)

    #Send sorted drop_point for target coords
    send_telem(drop_points, phase)
    adp = 1

    while phase == 'DROP':
         #Auto Pilot Check
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(1)
                mode = check_AUTO()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break

        #constantly updating waypoints
        print("Checking For Payload Drop")
        drop_points = haversine_high_frequency(drop_points, adp)
        adp += 1
        #once payload are dropped we go to mission end
        if len(drop_points) == 0:
            print("All Payloads Dropped To Targets")
            phase = 'END_MISSION'
            break
        

        time.sleep(.2)  #Adjust as needed for the update frequency

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()
