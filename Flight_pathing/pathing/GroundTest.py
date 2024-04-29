from pymavlink import mavutil, mavwp
import time
import csv
from Sorting_Distance import haversine_check

# Set the connection parameters (change accordingly)
connection_string = '/dev/ttyAMA0'
baudrate = 57600

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)                                       

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
    radius = 7
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
        print("Global Position: Lat={}, Lon={}, Alt={}".format(msg.lat, msg.lon, msg.alt))        
        # Sleep for a short duration to avoid busy-waiting
        time.sleep(0.1)
        
        return msg
    
def main():
    mode = None
    phase = None
    waypoints = [
    {"lat":   30.322588, "lon":  -97.602679},
    {"lat": 30.322291634213112, "lon": -97.6018262396288},
    ]   
    while mode is None:
        mode = check_AUTO()
        print('Waiting on Autopilot Mode')
        if mode == 'AUTO':
            phase = 'SEARCH'
            send_telem(waypoints,phase)
            break

    while phase == 'SEARCH':
        #Auto Pilot Check
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(.5)
                mode = check_AUTO(master)
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break

        #constantly updating waypoints
        print("Checking Waypoint Progress")
        waypoints = haversine_check(master, waypoints, 'Update_waypoints', None)        
    
        time.sleep(.2)  #Adjust as needed for the update frequency

        #once search is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            break




if __name__ == "__main__":
        main()
