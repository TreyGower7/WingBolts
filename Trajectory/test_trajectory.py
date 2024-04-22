from trajectory import projectile_range, release_point
#from Flight_pathing.pathing.Telempy import get_telem
import pytest
import random

H = 50
v_x = -20
v_y = 20

target_lat = 30.324385
target_long = -97.603339

current_long = -97.6029108
current_lat = 30.3249295

range = projectile_range(v_x, v_y, H)
RP = release_point(target_long, target_lat, range, current_long, current_lat)

print(RP)
print(f'{current_lat}, {current_long}')
print(f'{target_lat}, {target_long}')

def test_projectile_range():
    # examples
    assert(round(projectile_range(0.32373*922263.6876*10**-3, 0.20601*922263.6876*10**-3, H), 5) == 48.59608)
    assert(round(projectile_range(0.04905*1042941.427*10**-3, 0.15696*1042941.427*10**-3, H), 5) == 26.65038)
    assert(round(projectile_range(0.14715*885563.7*10**-3, 0.52974*885563.7*10**-3, H), 5) == 33.28176)
    
    with pytest.raises(TypeError):
        projectile_range(v_x, 'v_x' , H)
    with pytest.raises(TypeError):
        projectile_range('v_x','v_x', H)
    with pytest.raises(TypeError):
        projectile_range('v_x',v_y,H)
    with pytest.raises(TypeError):
        projectile_range(v_x, v_y, 'H')
    with pytest.raises(TypeError):
        projectile_range()


def test_release_point():
    assert(round(release_point(-97.60128486, 30.32378242, 48.59608301, -97.59957015, 30.32076102)[0], 4) == 54.3096)
    assert(round(release_point(-97.60128486, 30.32378242, 48.59608301, -97.59957015, 30.32076102)[1], 3) == -139.865)

    assert(round(release_point(-97.60128486, 30.32378242, 26.6504, -97.59957015, 30.32076102)[0], 3) == 43.478)
    assert(round(release_point(-97.60128486, 30.32378242, 26.6504, -97.59957015, 30.32076102)[1], 3) == -120.779)
 
    assert(round(release_point(-97.60128486, 30.32378242, 33.2818, -97.59957015, 30.32076102)[0], 4) == 46.7509)
    assert(round(release_point(-97.60128486, 30.32378242, 33.2818, -97.59957015, 30.32076102)[1], 3) == -126.547)

    with pytest.raises(TypeError):
        release_point('target_long', target_lat, range, current_long, current_lat)
    with pytest.raises(TypeError):
        release_point(target_long, target_lat)