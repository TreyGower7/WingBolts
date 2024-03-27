import random

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

# Example usage:
domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
coords = random_coords(domain)
print(coords)
