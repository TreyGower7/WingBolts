import time
from pymavlink import mavutil
import numpy as np
import math
import random

def random_coords(domain):
    """
    *********************
    ** Only Using For Sims **
    *********************
    Generate random latitude and longitude within a specified domain.

    Args:
    Tuple (min_lat, max_lat, min_lon, max_lon)

    Returns:
    Tuple (latitude, longitude)
    """
    min_lat, max_lat, min_lon, max_lon = domain
    lat = random.uniform(min_lat, max_lat)
    lon = random.uniform(min_lon, max_lon)
    coords = {'latitude': lat, 'longitude': lon}
    return coords

def get_telem():
    '''
    Gets Telemetry data from Pixhawk
    '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    coords = random_coords(domain)
    return coords

def projectile_range(v_x, v_y, H):
    """
    Using random numbers for the variables as placeholders until we find out how to get the data from Pixhawk
    This is a SUPER rough code straight from the research paper
    """

    # these are constant parameters that should be stored beforehand
    rho = 1.225 # kg/m^3 density of air
    Cd = 0.82 # drag coefficient, proportional to airspeed?

    # A does not include the grid fins yet
    A = 0.016214 # surface area of the payload in m^2 (2 in diameter, 3 in length)
    m = 0.181 # payload mass in kg (0.4 lb)

    q = 0.5*rho*Cd*A
    dt = 0.02 # time interval
    N = 3000 # max iterations

    iters = 0
    x = 0
    y = 0
    t = 0
    while (iters < N):

        if (y >= H):
            R = x
            break
        
        a_x = -(q/m)*v_x**2
        a_y = 9.81 - (q/m)*v_y**2

        v_x += a_x*dt
        v_y += a_y*dt

        x += v_x*dt + 0.5*a_x*dt**2
        y += v_y*dt + 0.5*a_y*dt**2

        print(iters, a_x, a_y, x, y, v_x, v_y)

        t += dt # total time, don't know what this is useful for?
    

        iters += 1

    return(R, y, x)

def release_point(target_long, target_lat, R, current_long, current_lat):
    z = (target_long - current_long)/(target_lat - current_lat)
    theta = math.atan(z)
    RP_lat = target_lat - R*math.sin(theta)
    RP_long = target_long - R*math.cos(theta)
    return(RP_lat, RP_long)


def geo_to_cartesian(latitude, longitude):
    # have to double check that this is how you calculate it
    r = 6371
    lat = math.radians(latitude)
    lon = math.radians(longitude)
    x = r*math.cos(lat)*math.cos(lon)
    y = r*math.cos(lat)*math.sin(lon)
    return(x,y)


if __name__ == "__main__":
    altitude = 45.72 # surveillance phase
    print(projectile_range())



