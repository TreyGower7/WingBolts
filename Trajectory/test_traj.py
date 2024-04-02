from trajectory import release_point, projectile_range, geo_to_cartesian

def main():
    v_y = 0
    v_x = 0
    H = 0
    target_lon = 0
    target_lat = 0
    current_lat = 0
    current_lon = 0
    range, time = projectile_range(v_y, v_x, H)
    RP_lat, RP_lon = release_point(target_lon. target_lat, range, current_lon, current_lat)
    RP_x, RP_y = geo_to_cartesian(RP_lat, RP_lon)
    target_x, target_y = geo_to_cartesian(target_lat, target_lon)
    xf = RP_x + v_x*time

    # how close is xf to target_x? 
    # yf should be 0 and target_y should also be 0 because it is flat on the ground



if __name__ == "__main__":
    main()

