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
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_lon, max_lon)
    return latitude, longitude

# Example usage:
domain = (30.320122, 30.324865, -97.603076, -97.598687)  # Boundaries for Arca
lat, lon = random_coords(domain)
coords = [lat, lon]

print(coords)
