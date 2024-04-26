from Sorting_Distance import haversine_check
distance = 0
firstWaypoints = [
        {"lat":   30.322588, "lon":  -97.602679},
        {"lat": 30.322291634213112, "lon": -97.6018262396288},
        {"lat":  30.323143653772693, "lon": -97.60142927270336},
        {"lat": 30.325269418344888, "lon": -97.60358765983898},
        {"lat": 30.32556423886435, "lon": -97.60242970541643},
        {"lat": 30.323148122665625, "lon": -97.60268795424491}
        ]


for i in range(len(firstWaypoints)):
    distance += haversine_check(None, firstWaypoints[i-1], 'Distance', firstWaypoints[i])
#Distance of one loop # after 3 nautical miles: 1 meter = 0.000539957 miles
nautMiles = distance * 0.539957
total_naut_miles = 0
numofloops = 0
while total_naut_miles <= 3:
    total_naut_miles += nautMiles
    numofloops += 1;
    print(total_naut_miles)
print(numofloops)

for i in range(numofloops):
    firstWaypoints.append(firstWaypoints)