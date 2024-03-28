import random
"""
Simulates input of random coords at Arca into pixhawk 

*********************
** Only Using For Sims **
*********************

"""

__author__ = "Trey Gower"

def random_coords(domain):
    """
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

def main():
    ''' Main entry point of the app '''
    domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
    coords = random_coords(domain)
    print(coords)
    print(f'Formatted: {coords["latitude"]}, {coords["longitude"]}')
if __name__ == "__main__":
    ''' This is executed when run from the command line '''
    main()

