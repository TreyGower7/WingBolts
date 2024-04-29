from pymavlink import mavutil, mavwp
import time
import csv
import math

# Set the connection parameters (change accordingly)
connection_string = '/dev/ttyAMA0'
baudrate = 57600

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)                                       

def haversine_check(waypoints, use, ref_waypoint):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers

    if use == 'Update_waypoints' or use == 'DROP':
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
        if distance <= 0.0021336: #7 feet
            waypoints.pop(0)  # Remove the reached waypoint
            return 'DROP_SIGNAL', waypoints
        else:
            return 'WAIT', None
            
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
    
def send_telem(waypoints,phase):
    wp = mavwp.MAVWPLoader()   
    altitude = altitude_handle(phase)                                                 
    seq = 1
    frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    radius = 10
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

def receive_telem():
    '''
    receives telemetry data from pixhawk to pi
    '''
    #message
    msg = master.recv_match(type=['GLOBAL_POSITION_INT'],blocking=True)             
    # Check if message is not None
    if msg:
        print("Global Position: Lat={}, Lon={}, Alt={}".format(msg.lat, msg.lon, float(msg.alt)/1000))        
        # Sleep for a short duration to avoid busy-waiting
        time.sleep(0.1)
        
        return msg
    
def main():
    mode = None
    phase = None
    #waypoints = [
    #    {"lat": 30.323221, "lon":  -97.602798},
    #    {"lat": 30.323180, "lon": -97.601598},
    #    {"lat": 30.323715, "lon": -97.603007},
    #    {"lat": 30.324627, "lon": -97.602312},
    #    {"lat": 30.325696, "lon": -97.603918},
    #]   
    waypoints = [
        {"lat":   30.32378824187, "lon":  -97.6036873380},
        #{"lat":   30.3243808844, "lon":  -97.603326202},
        #{"lat": 30.3241018240, "lon": -97.603156859160},
        #{"lat": 30.32356625003424, "lon": -97.60290823014489},
    ]    
    send_telem(waypoints,'search')
    
    while mode is None:
        mode = check_AUTO()
        print('Waiting on Autopilot Mode')
        if mode == 'AUTO':
            phase = 'SEARCH'
            break
            
    while phase == 'SEARCH':
    #Auto Pilot Check
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
    
        time.sleep(2)  #Adjust as needed for the update frequency

        #once search is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            break
    print('mission done')
    check_AUTO()

if __name__ == "__main__":
        main()
