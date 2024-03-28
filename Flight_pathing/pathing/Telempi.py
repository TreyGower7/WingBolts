from RandLatlon import random_coords
import numpy as np 
from pymavlink import mavutil

"""
Updating pixhawk from our ML model
"""

__author__ = "Trey Gower"

def get_telem():
    '''
    Gets Telemetry data from Pixhawk
    '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    coords = random_coords(domain)
    return coords

def send_telem(formatted_coords):
    '''
    sends telemetry data to pixhawk from pi
    '''
    
def main():
    ''' Main entry point of the app '''
    coords = get_telem()
if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()