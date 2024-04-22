from pymavlink import mavutil
import random
import time
from Flight_pathing.pathing.Telempy import send_telem
from Flight_pathing.pathing.Sorting_Distance import sort_obj_waypoints



def Search_zigzag(master):
    alt = 76.2 #meters
    phase = 'surveillance'
    waypoints = [
    {"lat":   30.322588, "lon":  -97.602679},
    {"lat": 30.322319, "lon": -97.601799},
    {"lat":   30.323467, "lon": -97.601896},
    {"lat": 30.323625, "lon": -97.603752},
    {"lat": 30.324597, "lon": -97.602615},
    {"lat": 30.325245, "lon": -97.604256},
    ]   
    #populate waypoints for initial search phase
    for i in range(len(waypoints)):
        coords = {'latitude': waypoints[i]['lat'], 'longitude': waypoints[i]['lon']}
        send_telem(coords, phase)

    return waypoints

def predrop_phase(refinedobj_waypoints, phase):
    '''
    Sets the plane up for dropping the payload
    '''
    distressed_waypoints = []
    happy_waypoints = []

    #fly out to random point to prepare for payload drop
    reset_waypoint = {'lat': 30.323246847038178, 'lon': -97.60228430856947}
    send_telem(reset_waypoint, phase)
    print(f"Sending waypoint: ({reset_waypoint[i]['lat']}, {reset_waypoint[i]['lon']})")

    #Sort and send distressed targets
    #****Write these to a file to be saved***** 
    for i in range(len(refinedobj_waypoints)):
        if refinedobj_waypoints[i]['state'] == 'distressed':
            distressed_waypoints.append(refinedobj_waypoints[i])
        else:
            happy_waypoints.append(refinedobj_waypoints[i])

     #***Calculate drop points here in a loop and store them based on distressed_waypoints***
    #first drop point based on reset point, second drop point based on first object waypoint...
    drop_points = {'lat': 0, 'lon': 0}

    #Sort by distance
    drop_points = sort_obj_waypoints(reset_waypoint, drop_points)
    #Send sorted drop_point for target coords
    for i in range(len(drop_points)):
        #****Need to Add Loitering****
        coords = {'latitude': drop_points[i]['lat'], 'longitude': drop_points[i]['lon']}
        send_telem(coords, phase)
        print(f"Sending waypoint {i+1}: ({drop_points[i]['lat']}, {drop_points[i]['lon']})")
    
    return drop_points





