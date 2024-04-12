#import Listen
from Flight_pathing.pathing.Telempy import get_telem, send_telem
import time
from Search import Search_zigzag, check_waypoint

"""
Main script for connecting to pixhawk,
sending/recieving coordinates from raspberry pi to pixhawk 
and updating waypoints based on ML
"""

__author__ = "Trey Gower"

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
            send_telem(coords)
            break
        
    while phase_surveillance == True:
        check_waypoint(waypoints)
        coords = get_telem()
        send_telem(coords)

        time.sleep(5)  #Adjust as needed for the update frequency
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()