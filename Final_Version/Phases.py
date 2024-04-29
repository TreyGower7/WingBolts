from trajectory import traj_main



def Search_zigzag():
    waypoints = [
    {"lat":   30.3225355, "lon":  -97.6023138},
    {"lat": 30.3230727, "lon": -97.6009941},
    {"lat":  30.3256843, "lon": -97.6022387},
    {"lat": 30.3255546, "lon": -97.6036978},
    {"lat": 30.3224429, "lon": -97.6021528},
    {"lat": 30.3230542, "lon": -97.6006722},
    {"lat": 30.3257583, "lon": -97.6017988}
    {"lat": 30.3256102, "lon": -97.6032257}
    {"lat": 30.3225541, "lon": -97.6016378}
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





