from trajectory import projectile_range, release_point, get_telem

H = 45.72
t = 1073732*10**-3 # this is right
acc_x = 0.12753
acc_y = 0.35316
v_x = t*acc_x
v_y = t*acc_y

target_coords = get_telem()
target_long = target_coords['longitude']
target_lat = target_coords['latitude']

current_coords = get_telem()
assert(current_coords != target_coords)

current_long = current_coords['longitude']
current_lat = current_coords['latitude']

a_y = 9.81 - (0.0041710515/0.181)*v_y**2
print(round(a_y))

range = projectile_range(v_x, v_y, H)
RP = release_point(target_long, target_lat, range, current_long, current_lat)
