from Trajectory.trajectory import traj_main



def Search_zigzag():
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

    return waypoints

def predrop_phase(refinedobj_waypoints):
    '''
    Sets the plane up for dropping the payload
    '''
    distressed_waypoints = []
    happy_waypoints = []

    #fly out to random point to prepare for payload drop
    reset_waypoint = {'lat': 30.323246847038178, 'lon': -97.60228430856947}

    #Sort and send distressed targets
    #****Write these to a file to be saved***** 
    for i in range(len(refinedobj_waypoints)):
        if refinedobj_waypoints[i]['state'] == 'distressed':
            distressed_waypoints.append(refinedobj_waypoints[i])
        else:
            happy_waypoints.append(refinedobj_waypoints[i])

     #***Calculate drop points here in a loop and store them based on distressed_waypoints***
    #first drop point based on reset point, second drop point based on first object waypoint...
    #List of dictionaries format
    #Starting from the reset_waypoint
    drop_points = [reset_waypoint]
    current_lon = reset_waypoint['lon']
    current_lat = reset_waypoint['lat']
    for i in range(len(distressed_waypoints)):
        RP = traj_main(current_lon, current_lat, distressed_waypoints[i]['lon'], distressed_waypoints[i]['lat'])
        drop_points.append(RP)
        current_lon = RP['lon']
        current_lat = RP['lat'] 

    
    return drop_points





