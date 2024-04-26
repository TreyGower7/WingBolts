from Phases import Search_zigzag, predrop_phase
from Sorting_Distance import haversine_check, haversine_high_frequency
from Telempy import send_telem, check_AUTO, receive_telem
import time
from pymavlink import mavutil
import json

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
        mode = check_AUTO(master)
        print('Waiting on Autopilot Mode')
        if mode == 'AUTO':
            phase = 'PRE_MISSION'
            break

    distance = 0
    firstWaypoints = [
            {"lat":   30.322588, "lon":  -97.602679},
            {"lat": 30.322291634213112, "lon": -97.6018262396288},
            {"lat":  30.323143653772693, "lon": -97.60142927270336},
            {"lat": 30.325269418344888, "lon": -97.60358765983898},
            {"lat": 30.32556423886435, "lon": -97.60242970541643},
            {"lat": 30.323148122665625, "lon": -97.60268795424491}]
    firstWaypoints_copy = firstWaypoints
    for i in range(len(firstWaypoints)):
        distance += haversine_check(None, firstWaypoints[i-1], 'Distance', firstWaypoints[i])
    #Distance of one loop # after 3 nautical miles: 1 meter = 0.000539957 miles
    nautMiles = distance * 0.539957
    total_naut_miles = 0
    numofloops = 0
    while total_naut_miles <= 3:
        total_naut_miles += nautMiles
        numofloops += 1;
        print(total_naut_miles)
    for i in range(numofloops):
        send_telem(master, waypoints, phase)
        #For the Next loop
        firstWaypoints.append(firstWaypoints)

    while phase == 'PRE_MISSION':
        #Auto Pilot Check
        mode = check_AUTO(master)
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
        firstWaypoints = haversine_check(master, firstWaypoints, 'Update_waypoints', None)        

        time.sleep(.2)  #Adjust as needed for the update frequency

        #need to repopulate waypoints due to how I wrote the code
        if len(firstWaypoints) == 0 and pre != numofloops:
            print("All waypoints reached")
            pre += 1
            firstWaypoints = firstWaypoints_copy
            continue
        if len(firstWaypoints) == 0 and pre == numofloops:
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            #populate waypoints for initial search phase
            phase = 'SEARCH'
            send_telem(master, waypoints, phase)
            break


    while phase == 'SEARCH':
        #Auto Pilot Check
        mode = check_AUTO(master)
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
            phase = 'SURVEILLANCE'
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            #populate waypoints for initial search phase
            send_telem(master, waypoints, phase)
            break
    #Another phase that changes altitude
    while phase == 'SURVEILLANCE':
        #Auto Pilot Check
        mode = check_AUTO(master)
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
            phase = 'DROP'
            break

    #Get Waypoints from json file predrop setup and send to pixhawk
    with open('Final_Version/target_coords.json', 'r') as f:
        Obj_waypoints = json.loads(f)

    #Set the plane up for payload drop

    drop_points = predrop_phase(Obj_waypoints)

    #Send sorted drop_point for target coords
    send_telem(master, drop_points, phase)
    adp = 1

    while phase == 'DROP':
         #Auto Pilot Check
        mode = check_AUTO(master)
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(.5)
                mode = check_AUTO(master)
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break

        #constantly updating waypoints
        print("Checking For Payload Drop")
        drop_points = haversine_high_frequency(master, drop_points, adp)
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
