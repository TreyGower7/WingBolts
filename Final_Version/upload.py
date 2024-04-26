from pymavlink import mavutil
import time

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)
master.wait_heartbeat()
print(f"Heartbeat from system ({master.target_system}, {master.target_component})")

# Function to send waypoints to QGroundControl
def send_waypoints(connection, waypoints):
    # Clear existing mission items
    connection.waypoint_clear_all_send()
    time.sleep(1)

    # Add new waypoints
    for idx, waypoint in enumerate(waypoints):
        msg = connection.mav.mission_item_send(
            connection.target_system, connection.target_component,
            idx,              # Sequence
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # Frame
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,           # Command
            0,                # Current
            0,                # Autocontinue
            0, 0, 0,          # Params 1-3 (Hold time, Acceptance radius, Pass radius)
            waypoint['latitude'], waypoint['longitude'], waypoint['altitude']  # Params 4-6 (Latitude, Longitude, Altitude)
        )
        time.sleep(0.2)  # Add a small delay between each waypoint

# Example waypoints (latitude, longitude, altitude in meters)
waypoints = [
    {'latitude': 47.641468, 'longitude': -122.140165, 'altitude': 10},
    {'latitude': 47.641529, 'longitude': -122.140001, 'altitude': 20},
    {'latitude': 47.641476, 'longitude': -122.139891, 'altitude': 30}
]

# Connection to QGroundControl

# Send waypoints
send_waypoints(master, waypoints)

# Close connection
master.close()
