import math
from pyproj import Proj, transform
from Telempy import receive_telem

def projectile_range(v_x, v_y, H):
    """
    Using random numbers for the variables as placeholders until we find out how to get the data from Pixhawk
    This is a SUPER rough code straight from the research paper
    """

    # these are constant parameters that should be stored beforehand
    rho = 1.225 # kg/m^3 density of air
    Cd = 0.82 # drag coefficient, proportional to airspeed?

    # A does not include the grid fins yet
    A = 0.016214 # surface area of the payload in m^2 (2 in diameter, 3 in length)
    m = 0.181 # payload mass in kg (0.4 lb)

    q = 0.5*rho*Cd*A
    dt = 0.02 # time interval
    N = 3000 # max iterations

    iters = 0
    x = 0
    y = 0
    if (v_x < -7) :
        v_x = abs(v_x)
    
    if( v_y < -14):
        v_y = abs(v_y)

    while (iters < N):

        if (y >= H):
            R = x
            break
        
        a_x = -(q/m)*(v_x)**2
        a_y = 9.81 - (q/m)*(v_y)**2

        v_x += a_x*dt
        v_y += a_y*dt

        x += v_x*dt + 0.5*a_x*dt**2
        y += v_y*dt + 0.5*a_y*dt**2

        iters += 1

    return R

def geo_2_cart(lat, lon):
    input_proj = Proj(proj='latlong', datum='WGS84')
    output_proj = Proj(proj='utm', zone=10, ellps='WGS84')
    x, y = transform(input_proj, output_proj, lon, lat)
    return x,y

def cart_2_geo(x, y):
    input_proj = Proj(proj='utm', zone=10, ellps='WGS84')
    output_proj = Proj(proj='latlong', datum='WGS84')
    lon, lat = transform(input_proj, output_proj, x, y)

    return lon, lat

def release_point(target_long, target_lat, R, current_long, current_lat):
    c_x, c_y = geo_2_cart(current_lat, current_long)
    t_x, t_y = geo_2_cart(target_lat, target_long)
    z = (t_y - c_y)/(t_x - c_x)
    theta = math.atan(z)
    RP_x = t_x + R*math.cos(theta)
    RP_y = t_y + R*math.sin(theta)
    RP_long, RP_lat = cart_2_geo(RP_x, RP_y)
    return {'lat': RP_lat, 'lon': RP_long}

def traj_main(current_lon, current_lat, target_long, target_lat):

    pix = receive_telem()
    H = pix.relative_alt * 10^-3
    vx = pix.vx * 10^-2
    vy = pix.vy * 10^-2 # it says vz, is the speed positive down?
    range = projectile_range(vx, vy, H)

    # this is fed to the servo and when our current location matches this, 
   # drop the payload
    RP = release_point(target_long, target_lat, range, current_lon, current_lat)
    return RP
   




