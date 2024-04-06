import numpy as np
import math

def projectile_range():
    """
    Using dummy variables until we find out how to get the data from Pixhawk
    """
    # all of the following are recorded at a given instant and should come from Pixhawk

    u = 1; # aircraft velocity (relative to ground) (groundspeed?)
    H = 1; # aircraft altitude (above ground level)
    w = 1; # wind speed (relative to ground)

    # these are constant parameters that should be stored beforehand
    rho = 1; # density of air
    Cd = 1; # drag coefficient
    A = 1; # surface area of the payload
    m = 1; # payload mass

    q = 0.5*rho*Cd*A;
    dt = 0.02; # time interval
    N = 3000; # max iterations

    iters = 0;
    v_x = 1;
    v_y = 1;
    x = 0;
    y = 0;
    t = 0;
    while (iters < N):
        a_x = -(q/m)*v_x**2;
        a_y = 9.81 - (q/m)*v_y**2;
        new_v_x = v_x + a_x*dt;
        new_v_y = v_y + a_y*dt;
        new_x = x + v_x*dt + 0.5*a_x*dt**2;
        new_y = y + v_y*dt + 0.5*a_y*dt**2;
        x = new_x;
        y = new_y;
        t += dt; # total time, don't know what this is useful for?
    
        if (y == H):
            R = x;
            break
        else:
            continue

    return(R)

if __name__ == "__main__":
    print(projectile_range())



