from Flight_pathing.pathing.Phases import Search_zigzag, predrop_phase
from Flight_pathing.pathing.Sorting_Distance import haversine_check, sort_obj_waypoints, haversine_high_frequency
from Flight_pathing.pathing.Telempy import send_telem, receive_telem, haversine_check, check_AUTO, get_obj_coords
import math
import time
from pymavlink import mavutil, mavwp

"""
Main script for connecting to pixhawk,
sending/recieving coordinates from raspberry pi to pixhawk 
and updating waypoints based on ML
"""

__author__ = "Trey Gower"

connection_string = '/dev/ttyAMA0' #Pin connectors for Pi
baudrate = 57600  

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)

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
            #populate waypoints for initial search phase
            phase = 'SEARCH'
            send_telem(waypoints, phase)
            break

    #saves last waypoint for sorting alg
    last_waypoint = waypoints[-1]

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
            #****Need to Add Loitering****
            send_telem(Obj_waypoints, phase)
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
    drop_points = predrop_phase(refinedobj_waypoints)

    #Send sorted drop_point for target coords
    send_telem(drop_points, phase)

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
