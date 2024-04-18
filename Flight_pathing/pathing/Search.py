from pymavlink import mavutil
import random
import time
from Flight_pathing.pathing.Telempy import send_telem, receive_telem


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

def main():


if 




