from Random_Lat_lon import random_coords
import numpy as np 
import pymavlink as pml



#generate random Arca Lat and lon
domain = (30.320122, 30.324865, -97.603076, -97.598687) 
coords = random_coords(domain)

def format_telem(coords):
    '''
    Function formates the telemetry data to be inserted into our ML model 
    '''
    coords = np.column_stack(coords[0], coords[1])