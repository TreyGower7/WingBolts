import sys
import math
import clr
import time
import System
from System import Byte

clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
from MissionPlanner.Utilities import Locationwp
clr.AddReference("MAVLink") # includes the Utilities class
import MAVLink

idmavcmd = MAVLink.MAV_CMD.WAYPOINT
id = int(idmavcmd)

def altitude_handle(phase):
    '''
    handles the altitude inputs to the plane
    '''
    #Altitudes are in meters
    if phase == 'search':
        return 91.44
    if phase == 'surveillance':
        return 45.72
    
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

def Search_zigzag():
    '''
    Search phase for targets
    '''
    phase = 'surveillance'
    altitude = altitude_handle(phase)#meters

    waypoints = [
        {"lat": 30.323221, "lon": -97.602798, "alt": altitude},
        {"lat": 30.323180, "lon": -97.601598,"alt": altitude},
        {"lat": 30.323715, "lon": -97.603007,"alt": altitude},
        {"lat": 30.324627, "lon": -97.602312,"alt": altitude},
        {"lat": 30.325696, "lon": -97.603918,"alt": altitude},
    ]
    

    return waypoints

def send_telem(waypoints):
    '''
    sends telemetry data to pixhawk from pi
    '''
    
        # Upload waypoints in a loop
    for i, point in enumerate(waypoints):
        wp = Locationwp().Set(point['lat'], point['lon'], point['alt'], id)
        MAV.setWP(wp, i + 2, MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT)
        print(f"Uploaded waypoint {i + 1}: ({point['lat']}, {point['lon']}, {point['alt']})")
    # Set the flight mode to "auto"
    MAV.setMode("AUTO")
    print("Flight mode set to AUTO.")
    # Final acknowledgment
    MAV.setWPACK()
    print("Waypoints set and uploaded successfully.")
   
    
# Set home location
home = Locationwp().Set(30.324026609525255, -97.60331097904584, 0, id)

# Define takeoff location
to = Locationwp()
Locationwp.id.SetValue(to, int(MAVLink.MAV_CMD.TAKEOFF))
Locationwp.p1.SetValue(to, 10)
Locationwp.alt.SetValue(to, 100)
print("upload home - reset on arm")
MAV.setWP(home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
print("upload to")
MAV.setWP(to,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
# Define search waypoints
waypoints = Search_zigzag()
# Send Telemetry
send_telem(waypoints)




