from trajectory import projectile_range, release_point, get_telem, geo_to_cartesian

import pytest

H = 45.72
t = 885563.7*10**-3 # this is right
acc_x = 0.14715
acc_y = 0.52974
v_x = t*acc_x
v_y = t*acc_y

target_coords = get_telem()
target_long = target_coords['longitude']
target_lat = target_coords['latitude']


current_coords = get_telem()

current_long = current_coords['longitude']
current_lat = current_coords['latitude']

a_y = 9.81 - (0.0041710515/0.181)*v_y**2

[range, y, x] = projectile_range(v_x, v_y, H)
[RP_lat, RP_long] = release_point(target_long, target_lat, range, current_long, current_lat)

print(RP_lat, RP_long)
print(current_coords)
print(target_coords) 
def test_projectile_range():
    assert(current_coords != target_coords)
    assert(x == range)
    assert(y >= H)

    # examples
    assert(round(projectile_range(0.32373*922263.6876*10**-3, 0.20601*922263.6876*10**-3, H)[0], 5) == 48.59608)
    assert(round(projectile_range(0.04905*1042941.427*10**-3, 0.15696*1042941.427*10**-3, H)[0], 5) == 26.65038)
    assert(round(projectile_range(0.14715*885563.7*10**-3, 0.52974*885563.7*10**-3, H)[0], 5) == 33.28176)

def test_release_point():
    assert(round(release_point(-97.60128486, 30.32378242, 48.59608301, -97.59957015, 30.32076102)[0], 4) == 54.3096)
    assert(round(release_point(-97.60128486, 30.32378242, 48.59608301, -97.59957015, 30.32076102)[1], 3) == -139.865)

    assert(round(release_point(-97.60128486, 30.32378242, 26.6504, -97.59957015, 30.32076102)[0], 3) == 43.478)
    assert(round(release_point(-97.60128486, 30.32378242, 26.6504, -97.59957015, 30.32076102)[1], 3) == -120.779)
 
    assert(round(release_point(-97.60128486, 30.32378242, 33.2818, -97.59957015, 30.32076102)[0], 4) == 46.7509)
    assert(round(release_point(-97.60128486, 30.32378242, 33.2818, -97.59957015, 30.32076102)[1], 3) == -126.547)
    
    