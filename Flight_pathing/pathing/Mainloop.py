#import Listen
from Telempi import get_telem
import time
"""
Main script for connecting to pixhawk then 
sending/recieving coordinates from raspberry pi to pixhawk 
and upadting waypoints based on ML
"""

__author__ = "Trey Gower"

def main():
    """ Main entry point of the app """

    #Listen()     #connect pixhawk and pi
    a=2
    #need to define some condition to stop looping 
    while a != 1:
        coords = get_telem()
        print(f'{coords["latitude"]}, {coords["longitude"]}')
        time.sleep(2)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()