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
domain = (-90, 90, -180, 180)  # Entire globe
lat, lon = random_coords(domain)
print("Latitude:", lat)
print("Longitude:", lon)
