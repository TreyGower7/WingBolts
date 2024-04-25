from Phases import Search_zigzag, predrop_phase
from Sorting_Distance import haversine_check, haversine_high_frequency
from Telempy import send_telem, haversine_check, check_GUIDED, get_obj_coords
import time
from pymavlink import mavutil

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

def main():
    ''' Main Func '''
    phase = None
    mode = None
    Obj_waypoints = []
    #Ensures we manually set the mode to AUTO
    while mode is None:
        mode = check_GUIDED()
        print('Waiting on Autopilot Mode')
        if mode == 'GUIDED':
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            #populate waypoints for initial search phase
            phase = 'SEARCH'
            send_telem(master, waypoints, phase)
            break

    while phase == 'SEARCH':
        #Auto Pilot Check
        mode = check_GUIDED()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(.5)
                mode = check_GUIDED()
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
            phase = 'DROP'
            break

    #Get Waypoints from csv file predrop setup and send to pixhawk
    Obj_waypoints = 

    #Set the plane up for payload drop

    drop_points = predrop_phase(Obj_waypoints)

    #Send sorted drop_point for target coords
    send_telem(master, drop_points, phase)

    while phase == 'DROP':
         #Auto Pilot Check
        mode = check_GUIDED()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(.5)
                mode = check_GUIDED()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break

        #constantly updating waypoints
        print("Checking For Payload Drop")
        drop_points = haversine_high_frequency(master, drop_points)

        #once payload are dropped we go to mission end
        if len(drop_points) == 0:
            print("All Payloads Dropped To Targets")
            phase = 'END_MISSION'
            break
        

        time.sleep(.2)  #Adjust as needed for the update frequency

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()
