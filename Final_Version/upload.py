from pymavlink import mavutil
import time

connection_string = '/dev/ttyAMA0' #Pin connectors for Pi
#connection_string = '/dev/ttys039' #virtual connection for testing

baudrate = 57600  
# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)
master.wait_heartbeat()
print(f"Heartbeat from system ({master.target_system}, {master.target_component})")

# Function to send waypoints to QGroundControl
def send_waypoints(waypoints):
    # Clear existing mission items
    connection.waypoint_clear_all_send()
    time.sleep(1)
    # Add new waypoints
    for idx, waypoint in enumerate(waypoints):
        msg = mavutil.mavlink.MAVLink_mission_item_int_message(
            1,              # Target system
            1,              # Target component
            idx,            # Sequence
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # Frame
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,   # Command
            0,              # Current
            1,              # Autocontinue
            0, 0, 0,        # Params 1-3 (Hold time, Acceptance radius, Pass radius)
            int(waypoint['latitude'] * 1e7),       # Latitude (in degrees * 1e7)
            int(waypoint['longitude'] * 1e7),      # Longitude (in degrees * 1e7)
            waypoint['altitude'] * 1000,           # Altitude (in meters * 1000)
            0               # Mission type
        )
        master.mav.send(msg)
        time.sleep(0.2)  # Add a small delay between each waypoint

# Example waypoints (latitude, longitude, altitude in meters)
waypoints = [
    {'latitude': 47.641468, 'longitude': -122.140165, 'altitude': 10},
    {'latitude': 47.641529, 'longitude': -122.140001, 'altitude': 20},
    {'latitude': 47.641476, 'longitude': -122.139891, 'altitude': 30}
]

# Send waypoints
send_waypoints(waypoints)

# Close connection
master.close()
