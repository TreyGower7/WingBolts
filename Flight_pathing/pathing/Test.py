import math
#from Telempy import receive_telem

def haversine_check(waypoints, use, ref_waypoint):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers

    if use == 'Update_waypoints' or use == 'DROP':
        #get current position
        #msg = receive_telem()
        current_lat = ref_waypoint['lat']
        current_lon = ref_waypoint['lon']
        waypoint_lat = waypoints[0]['lat']
        waypoint_lon = waypoints[0]['lon']
        
    if use == 'Distance':
        #only requires one point for input
        current_lat = ref_waypoint['lat']
        current_lon = ref_waypoint['lon']
        waypoint_lat = waypoints['lat']
        waypoint_lon = waypoints['lon']
       
    # Convert latitude and longitude from degrees to radians
    current_lat = math.radians(current_lat)
    current_lon = math.radians(current_lon)
    waypoint_lat = math.radians(waypoint_lat)
    waypoint_lon = math.radians(waypoint_lon)

    # Calculate the differences in latitude and longitude
    dlat = waypoint_lat - current_lat
    dlon = waypoint_lon - current_lon

    # Apply the Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(current_lat) * math.cos(waypoint_lat) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    print(distance)
    
    if use == 'Update_waypoints':
        if distance <= 6: #20 feet
            print(f"Reached waypoint: {waypoints[0][0]}, {waypoints[0][1]}")
            waypoints.pop(0)  # Remove the reached waypoint
        else:
            print(f'Distance from waypoint: {distance}')
        return waypoints
    if use == 'Distance':
        return distance
    
    if use == 'DROP':
        if distance <= 3: #9 feet
            waypoints.pop(0)  # Remove the reached waypoint
            return 'DROP_SIGNAL', waypoints
        else:
            return 'WAIT', None
waypoints = [
    {"lat":   30.322588, "lon":  -97.602679},
    {"lat":   30.3243808844, "lon":  -97.603326202},
    ]   
print(haversine_check(waypoints,'Update_waypoints',waypoints[1]))