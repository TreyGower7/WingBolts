import cv2
import numpy as np
import random as rd     # dont need for final code
import csv
import json

sensor_width_mm = 4.712 # Camera sensor width in millimeters
focal_length_mm = 16    # Focal length in millimeters

# Camera resolution (assuming square pixels for simplicity)
image_width = 2048
image_height = 1520


def get_bounding_box(log) -> np.array:
  '''
  Get list of four points within image resolution values that
  simulate a bounding box.

  Args: None
  Returns: list of lists of 2-dim coord. points
  '''
  x_vals = log['Bbox'][:4]
  y_vals = log['Bbox'][-4:]
  return np.array([[min(x_vals), min(y_vals)],[max(x_vals), min(y_vals)],[min(x_vals), max(y_vals)],[max(x_vals), max(y_vals)]], np.float32)

def get_object_center(bounding_box: np.array) -> np.array:
  '''
  Takes list of four bounding box values and returns the 
  center point.

  Args: 
    bounding_boxlist np.array[float] - list of four 2-dim coord points
  Returns:
    center point np.array[float] - center coordinates in list
  '''
  x_vals = []
  y_vals = []

  for i in range(len(bounding_box)):
    x_vals.append(bounding_box[i][0])
    y_vals.append(bounding_box[i][1])

  return np.array([[max(x_vals)+min(x_vals) / 2, max(y_vals)+min(y_vals) / 2]], dtype=np.float32) 

def get_unique_target():
  """
  TODO: read in gps coords for detections and group near coords- 10^-5 tolerance
  """


def main():
  # Read JSON file
  with open('webcam_bbox_log.json', 'r') as json_file:
    logs = json.load(json_file)

  # Calculate focal lengths in pixels
  horizontal_focal_length_px = (image_width * focal_length_mm) / sensor_width_mm
  vertical_focal_length_px = (image_height * focal_length_mm) / sensor_width_mm

  # Principal point (assuming the image center)
  principal_point = (image_width / 2, image_height / 2)

  target_info = []

  # Read in bounding box value
  for log in logs:
    # Read in current gps point of aircraft
    curr_gps = np.array([log['Location'][0], log['Location'][1]], dtype=np.float32) # dummy gps value for now
    # Read in camera height from the ground
    camera_height = log['Location'][2] # in units consistent with world coordinates

    image_points = get_bounding_box(log) 

    # Get center of bounding box
    object_center = get_object_center(image_points)

    # Camera matrix
    camera_matrix = np.array([[horizontal_focal_length_px, 0, principal_point[0]],
                              [0, vertical_focal_length_px, principal_point[1]],
                              [0, 0, 1]])

    # Define transformation matrix assuming the camera is pointing straight down
    rotation_matrix = np.eye(3)
    translation_vector = np.array([0, 0, camera_height])

    # Combine rotation and translation into a single matrix
    extrinsic_matrix = np.hstack((rotation_matrix, translation_vector.reshape(3, 1)))

    # Perform perspective transformation
    world_points = cv2.convertPointsToHomogeneous(object_center)
    world_points = cv2.perspectiveTransform(world_points, np.linalg.inv(camera_matrix) @ extrinsic_matrix)

    gps_est = curr_gps + world_points
    target_info.append({"lat": gps_est.tolist()[0][0][0], "lon": gps_est.tolist()[0][0][1], "class": log["Class"], "time": log["Time"]})

  # Extract field names from the first dictionary
  field_names = list(target_info[0].keys())

  with open('target_coords.csv', 'w', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=field_names)
      writer.writeheader()
      writer.writerows(target_info)
  
  print("wrote coords to csv")


if __name__ == '__main__':
  main()