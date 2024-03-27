import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def map_path(latlon_path):
    """
    right now this is not dynamic which might
    be okay for just visualizing the path. 
    TODO-> ask about that
    """
    # read in
    coords = pd.read_csv(latlon_path)
    coords.rename(columns={'GLOBAL_POSITION_INT.lat': 'Latitude'}, inplace=True)
    coords.rename(columns={'GLOBAL_POSITION_INT.lon': 'Longitude'}, inplace=True)

    # Create a bounding box to determine the size of the required map
    BBox = (coords.Longitude.min(),   coords.Longitude.max(),
            coords.Latitude.min(), coords.Latitude.max())

    # Plotting the points on the graph
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.plot(coords.Longitude, coords.Latitude)

    # Setting limits for the plot
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])

    filename = os.path.splitext(os.path.basename(latlon_path))[0]

    # titles and axis labels
    plt.title(filename+" Flight Path")
    plt.xlabel("Longitude Coordinates")
    plt.ylabel("Latitude Coordinates")

    plt.savefig("maps/"+filename)


if __name__ == "__main__":
    map_path("flight_logs/latlon-0209.csv")
