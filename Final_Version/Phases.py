from trajectory import traj_main



def Search_zigzag():
    waypoints = [
    {"lat":   30.322588, "lon":  -97.602679},
    {"lat": 30.322291634213112, "lon": -97.6018262396288},
    {"lat":  30.323143653772693, "lon": -97.60142927270336},
    {"lat": 30.325269418344888, "lon": -97.60358765983898},
    {"lat": 30.32556423886435, "lon": -97.60242970541643},
    {"lat": 30.323148122665625, "lon": -97.60268795424491},
    #Repeat once more 
    {"lat":   30.322588, "lon":  -97.602679},
    {"lat": 30.322291634213112, "lon": -97.6018262396288},
    {"lat":  30.323143653772693, "lon": -97.60142927270336},
    {"lat": 30.325269418344888, "lon": -97.60358765983898},
    {"lat": 30.32556423886435, "lon": -97.60242970541643},
    {"lat": 30.323148122665625, "lon": -97.60268795424491},
    ]   

    return waypoints


def predrop_phase(obj_waypoints):
    '''
    Sets the plane up for dropping the payload
    '''
    sad_waypoints = []
    happy_waypoints = []

    #fly out to random point to prepare for payload drop
    reset_waypoint = {'lat': 30.322416459788805, 'lon': -97.60161890138745}

    #Sort and send distressed targets

    #****Write these to a file to be saved***** 
    for i in range(len(obj_waypoints)):
        if obj_waypoints[i]['state'] == 'sad':
            sad_waypoints.append(obj_waypoints[i])
        else:
            happy_waypoints.append(obj_waypoints[i])

     #***Calculate drop points here in a loop and store them based on distressed_waypoints***
    #first drop point based on reset point, second drop point based on first object waypoint...
    #List of dictionaries format
    #Starting from the reset_waypoint
    drop_points = [reset_waypoint]
    current_lon = reset_waypoint['lon']
    current_lat = reset_waypoint['lat']
    for i in range(len(sad_waypoints)):
        RP = traj_main(current_lon, current_lat, sad_waypoints[i]['lon'], sad_waypoints[i]['lat'])
        drop_points.append(RP)
        current_lon = RP['lon']
        current_lat = RP['lat'] 

    
    return drop_points





