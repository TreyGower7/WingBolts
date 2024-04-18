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
    coords = {'lat': lat, 'lon': lon}
    return coords


def get_obj_coords():
    '''
    Gets Telemetry data from Pixhawk
    '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    coords = random_coords(domain)
    return coords

def haversine_check(waypoints, use, ref_waypoint):
    '''
    Calulates how close plane is to waypoint using angular seperation and the earths radius
    '''
    R = 6371.0  # Radius of the Earth in kilometers
   

    if use == 'Distance':
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

def sort_obj_waypoints(reference_waypoint, Obj_waypoints):
    '''
    sort the waypoints of the objects from closest to farthest
    '''
    
    #Calculate distances and store them along with object waypoints
    obj_distances = [(waypoint, haversine_check(waypoint, 'Distance', reference_waypoint)) for waypoint in Obj_waypoints]
    distances = [(haversine_check(waypoint, 'Distance', reference_waypoint)) for waypoint in Obj_waypoints]

    #Sort the object waypoints based on distances
    sorted_obj = [waypoint for waypoint, _ in sorted(obj_distances, key=lambda x: x[1])]

    print(f'{distances}\n')
    print(f'{obj_distances}\n')

    return sorted_obj

def main():
    Obj_waypoints = []

    waypoints = [
    {"lat":   30.323221, "lon":  -97.602798},
    {"lat": 30.323180, "lon": -97.601598},
    {"lat":   30.323715, "lon": -97.603007},
    {"lat": 30.324627, "lon": -97.602312},
    {"lat": 30.325696, "lon": -97.603918},
    ]   

    last_waypoint= waypoints[-1]
    for i in range(6): #generates 6 random objects
        Obj_waypoints.append(get_obj_coords())

            #Sorting Algorithmn
    print(f'{Obj_waypoints}\n')
    print('\nsorted:')
    print(sort_obj_waypoints(last_waypoint,Obj_waypoints))
if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()