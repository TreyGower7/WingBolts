from Flight_pathing.pathing.RandLatlon import random_coords
import numpy as np 
import pymavlink as pml

"""
Updating pixhawk from out ML model
"""

__author__ = "Trey Gower"

'''

'''
def get_telem():
    '''
    Gets Telemetry data from Pixhawk
    '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    return random_coords(domain)


def format_telem(coords):
    '''
    Function formates the telemetry data to be inserted into our ML model 
    '''
    coords = np.column_stack(coords[0], coords[1])

def main():
    ''' Main entry point of the app '''
    coords = get_telem()
    format_telem(coords)

if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()