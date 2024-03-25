import numpy as np
import math

def projectile_range():
    """
    Using dummy variables until we find out how to get the data from Pixhawk
    """
    # all of the following are recorded at a given instant and should come from Pixhawk
    # idk why the paper said it needed these? not used in the code?

    u = 1 # aircraft velocity (relative to ground) (groundspeed?)
    H = 1 # aircraft altitude (above ground level)
    w = 1 # wind speed (relative to ground)

    # these are constant parameters that should be stored beforehand
    rho = 0 # density of air
    Cd = 0 # drag coefficient
    A = 0 # surface area of the payload
    m = 1 # payload mass

    q = 0.5*rho*Cd*A
    dt = 0.02 # time interval
    N = 3000 # max iterations

    iters = 0
    v_x = 0
    v_y = 0
    x = 1
    y = 1
    t = 0
    while (iters < N):
        a_x = -(q/m)*v_x**2
        a_y = 9.81 - (q/m)*v_y**2

        v_x += a_x*dt
        v_y += a_y*dt

        x += v_x*dt + 0.5*a_x*dt**2
        y += v_y*dt + 0.5*a_y*dt**2

        t += dt # total time, don't know what this is useful for?
    
        if (y == H):
            R = x
            break
        else:
            continue
        iters += 1

    return(R)

def release_point(target_long, target_lat, R, current_long, current_lat):
    z = (target_long - current_long)/(target_lat - current_lat)
    theta = math.atan(z)
    RP_lat = target_lat - R*math.sin(theta)
    RP_long = target_long - R*math.cos(theta)
    return(RP_lat, RP_long)


if __name__ == "__main__":
    print(projectile_range())



