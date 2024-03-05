# This script takes a .csv file of lat and lon 
# gps coordinates downloaded from UAV Log Viewer
# and plots them on a Google Maps .html file

import gmplot

def parse_data(csv_file: str) -> list:
  '''
  Takes a csv file containing aircraft gps lats and lons
  and returns a list of latitude floats and a list of
  longitude floats.

  Args: 
    csv_file (Str): name of .csv file containing lat/long
                    coords from UAV Log Viewer
  
  Returns:
    lats (list[float]): list of latitude values
    lons (list[float]): list of longitude values
  '''
  lats = []
  lons = []

  # parse file and clean data  
  with open(csv_file) as f:
    lines = f.readlines()
    for i in range(1,len(lines)): # start @ 1 to skip title row
      raw_data = lines[i].split(',') # split values into list
      lats.append(float(raw_data[2].strip())) # append stripped string
      lons.append(float(raw_data[3].strip()))
  return lats,lons

def print_data(lats: list, lons: list) -> None:
  '''
  Takes two equal length lists of values and prints
  them to terminal in pairs.

  Args:
    lats (list): list of values
    lons (list): list of values
  
  Returns:
    None (prints pairs to terminal)
  '''
 # print data
  if(len(lats) == len(lons)):
    for i in range(len(lats)):
      print(lats[i], lons[i])

def main():
  # input and outpul file names
  csv_file = 'gps_data.csv'
  output_file = 'aircraft_path.html'

  # extract lat and lon values
  lats,lons = parse_data(csv_file)
  
  #print_data(lats,lons)

  # create map and plot coords
  gmap = gmplot.GoogleMapPlotter(lats[0], lons[0],17)
  gmap.plot(lats, lons, edge_width=4, color='red')
  gmap.draw(output_file)

if __name__ == '__main__':
  main()
