from Flight_pathing.pathing.Phases import Search_zigzag
from Flight_pathing.pathing.Sorting_Distance import haversine_check, sort_obj_waypoints, drop_line
from Flight_pathing.pathing.Telempy import send_telem, receive_telem, haversine_check, get_telem, check_AUTO
import math
import time
from pymavlink import mavutil, mavwp

"""
Main script for connecting to pixhawk,
sending/recieving coordinates from raspberry pi to pixhawk 
and updating waypoints based on ML
"""

__author__ = "Trey Gower"

def main():
    ''' Main Func '''
    phase = None
    mode = None

    #Ensures we manually set the mode to AUTO
    while mode is None:
        mode = check_AUTO()
        if mode == 'AUTO':
            #Populate Coordinates for Search phase
            waypoints = Search_zigzag()
            phase = 'search'
            break

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
        waypoints = haversine_check(waypoints)
        time.sleep(.2)  #Adjust as needed for the update frequency
        
        #***Check target recognition for waypoints of objects***

        #once zig zag is complete we go to next phase
        if len(waypoints) == 0:
            print("All waypoints reached")
            phase = 'surveillance'
             #first random point
            coords = get_telem()
            send_telem(coords, phase)
            break
        
    while phase == 'surveillance':
        mode = check_AUTO()
        if mode != 'AUTO':
            while mode != 'AUTO':
                print('Change Mode Back to Auto')
                time.sleep(.5)
                mode = check_AUTO()
                if mode == 'AUTO':
                    print('Mode is Back to Auto')
                    break
        haversine_check(coords)
        coords = get_telem()
        send_telem(coords, phase)

        time.sleep(.2)  #Adjust as needed for the update frequency

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()
