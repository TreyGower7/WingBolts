from pymavlink import mavutil, mavwp
import time
import csv

# Set the connection parameters (change accordingly)
connection_string = '/dev/ttyAMA0'
baudrate = 57600

# Connect to the Pixhawk
master = mavutil.mavlink_connection(connection_string, baud=baudrate)                                       

def check_GUIDED(master):
    '''
    Checks if the mode is in Guided mode
    '''
   # Request current flight mode
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_REQUEST_FLIGHT_MODE, 0, 0, 0, 0, 0, 0, 0, 0)
    # Wait for response
    msg = master.recv_match(type='COMMAND_ACK', blocking=True)
    if msg and msg.command == mavutil.mavlink.MAV_CMD_REQUEST_FLIGHT_MODE:
        print("Current flight mode:", mavutil.mavlink.enums['MAV_MODE_FLAG'][msg.param1].name)
    else:
        print("Failed to retrieve flight mode")
    return msg

#*******Tested and Working*******  
def altitude_handle(phase):
    '''
    handles the altitude inputs to the plane
    '''
    #Altitudes are in meters
    if phase == 'search':
        return 91.44
    if phase == 'surveillance':
        return 45.72  
    
def send_telem(waypoints,phase):
    altitude = altitude_handle(phase)                                                 
       # Clear existing waypoints
    master.mav.mission_clear_all_send(
        master.target_system, master.target_component)
    time.sleep(1)

    # Send new waypoints
    seq = 0
    for i in range(len(waypoints)):
        master.mav.mission_item_send(
            master.target_system, master.target_component,
            seq,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0, 0, 0, 0,
            waypoints[i]['lat'], waypoints[i]['lon'], altitude)
        seq += 1
        time.sleep(0.2)  # Add a small delay to ensure waypoints are sent sequentially 
    while True:
        msg = master.recv_match(type=['MISSION_ACK'], blocking=True)
        if msg:
            print("Waypoints updated successfully")
            break

def receive_telem():
    '''
    receives telemetry data from pixhawk to pi
    '''
    #message
    msg = master.recv_match(type=['GLOBAL_POSITION_INT'],blocking=True)             
    # Check if message is not None
    if msg:
        print("Global Position: Lat={}, Lon={}, Alt={}".format(msg.lat, msg.lon, msg.alt))        
        # Sleep for a short duration to avoid busy-waiting
        time.sleep(0.1)
        
        return msg
    
def main():
    waypoints = [
        {"lat": 30.323221, "lon":  -97.602798},
        {"lat": 30.323180, "lon": -97.601598},
        {"lat": 30.323715, "lon": -97.603007},
        {"lat": 30.324627, "lon": -97.602312},
        {"lat": 30.325696, "lon": -97.603918},
    ]   

    send_telem(waypoints,'search')

    # Define the filename
    filename = 'Telem_Test.csv'

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["lat", "lon", "alt", "Vx", "Vy", "Vz"])  # Write header
        for i in range(20):
            msg = receive_telem()  # Assuming receive_telem() returns telemetry data
            row = [msg.lat, msg.lon, msg.alt, msg.vx, msg.vy, msg.vz]  # Create row of data
            writer.writerow(row)  # Write row to CSV file
    msg = check_GUIDED
    print(msg)

if __name__ == "__main__":
        main()
