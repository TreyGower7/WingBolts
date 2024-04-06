#include <iostream>
#include <cmath>
#include <vector>


using namespace std;

float projectile_range(float v_x, float v_y, float H) {
    float rho = 1.225;
    float Cd = 0;
    float A = 0;
    float m = 1;

    float q = 0.5 * rho * Cd * A;
    float dt = 0.02;
    int N = 3000;

    int iters = 0;
    float x = 0;
    float y = 0;
    float t = 0;
    float R = 0;

    while (iters < N){
        float a_x = -(q/m)*v_x*v_x;
        float a_y = 9.81 - (q/m)*v_y*v_y;

        v_x += a_x*dt;
        v_y += a_y *dt;

        x += v_x *dt + 0.5 * a_x *dt * dt;
        y += v_y *dt + 0.5 * dt * dt;

        t += dt;

        if(y == H){
            R = x;
            break;
        }
        iters++;
    }
    return R;
}

// returns latitude release point, longitude release point:
vector<float> release_point( float target_long, float target_lat, float R, float current_long, float current_lat){
    float z = (target_long - current_long)/(target_lat - current_lat);
    float theta = atan(z);
    float RP_lat = target_lat - R*sin(theta);
    float RP_long = target_long - R*cos(theta);
    vector<float> RP(2);
    RP[0] = RP_lat;
    RP[1] = RP_long;
    return(RP);
}

// returns x, y:
vector<float> geo_to_cartesian(float latitude, float longitude){
    int r = 6371;
    // this depends on what the units of long/lat are! 
    // if in degrees:
    float lat = latitude * M_PI / 180;
    float lon = longitude * M_PI / 180;
    float x = r * cos(lat) * cos(lon);
    float y = r * cos(lat) * sin(lon);
    vector<float> cartesian(2);
    cartesian[0] = x;
    cartesian[1] = y;
    return(cartesian);
}

int main(){
    float H = 1;
    float v_x = 1;
    float v_y = 1;
    
    float target_long = 1;
    float target_lat = 1;
    float current_long = 1;
    float current_lat = 1;

    float range = projectile_range(v_x, v_y, H);
    vector<float> RP = release_point(target_long, target_lat, range, current_long, current_lat); // lat, lon
    cout << "Latitude of release point: " << RP[0] << endl;
    cout << "Longitude of release point: " << RP[1] << endl;
    return 0;
}    