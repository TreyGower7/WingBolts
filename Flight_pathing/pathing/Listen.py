from pymavlink import mavutil

# Connect to Pixhawk
connect = mavutil.mavlink_connection('udpin:localhost:14550')
#Waits for first heartbeat
connect.wait_heartbeat()

print(f'Heartbeat from system: {connect.target_system()}, component: {connect.target_component()} ')