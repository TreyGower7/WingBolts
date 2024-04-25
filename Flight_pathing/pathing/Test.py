from pymavlink import mavutil

def upload_waypoints(waypoints_file, connection):
    # Open the waypoint file
    with open(waypoints_file, 'r') as f:
        waypoints = f.readlines()

    # Connect to Pixhawk
    # Replace '/dev/ttyUSB0' with the appropriate serial port
    master = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

    # Clear existing waypoints
    master.mav.mission_clear_all_send(0, 0)

    # Parse and send waypoints
    seq = 0
    for line in waypoints:
        # Parse waypoint data from the file
        lat, lon, alt, hold_time = map(float, line.strip().split(','))

        # Send the waypoint to Pixhawk
        master.mav.mission_item_send(
            0, 0, seq,  # Target System, Component, Sequence
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0,  # Current, Autocontinue, Param 1-2
            0, 0, 0,  # Param 3-5
            lat, lon, alt  # Latitude, Longitude, Altitude
        )
        seq += 1

    # Wait for acknowledgment
    while True:
        msg = master.recv_match(type=['MISSION_ACK'], blocking=True)
        if msg:
            print("Waypoints updated successfully")
            break

# Example usage
waypoints_file = 'waypoints.txt'
connection = '/dev/ttyUSB0'  # Replace with appropriate serial port
upload_waypoints(waypoints_file, connection)
