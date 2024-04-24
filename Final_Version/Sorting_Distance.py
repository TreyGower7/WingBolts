from CompanionTelem import receive_telem
import math
from servo.servoscript import servo_activate
#*******Tested and Working*******
def haversine_check(waypoints, use, ref_waypoint):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers

    if use == 'Update_waypoints' or use == 'Drop':
        #get current position
        msg = receive_telem()
        current_lat = msg.lat
        current_lon = msg.lon
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
        
    if use == 'Update_waypoints':
        if distance < 0.003048: #10 feet
            print(f"Reached waypoint: {waypoints[0][0]}, {waypoints[0][1]}")
            waypoints.pop(0)  # Remove the reached waypoint
        else:
            print(f'Distance from waypoint: {distance}')
        return waypoints
    if use == 'Distance':
        return distance
    
    if use == 'DROP':
        if distance <= 0.0009144: #3 feet
            waypoints.pop(0)  # Remove the reached waypoint
            return 'DROP_SIGNAL', waypoints
        else:
            return 'WAIT', None

def haversine_high_frequency(drop_points):
    '''
    High frequency update of plane location for the most accurate dropping position
    '''
    while True:
        Signal, drop_points = haversine_check(drop_points, 'DROP', None)
        if Signal == 'DROP_SIGNAL':
            servo_activate()
            break
    return drop_points

#*******Tested and Working*******
def sort_obj_waypoints(reference_waypoint, Obj_waypoints): 
    '''
    sort the waypoints of the objects from closest to farthest
    '''
    
    #Calculate distances and store them along with object waypoints
    obj_distances = [(waypoint, haversine_check(waypoint, 'Distance', reference_waypoint)) for waypoint in Obj_waypoints]
    
    #Sort the object waypoints based on distances
    sorted_obj = [waypoint for waypoint, _ in sorted(obj_distances, key=lambda x: x[1])]
    
    return sorted_obj
