import cv2
import numpy as np
import random as rd     # dont need for final code
from ..Flight_pathing.pathing import Telempy as tp
from tflite_webcam_bboxes import bbox_data

sensor_width_mm = 4.712 # Camera sensor width in millimeters
focal_length_mm = 16    # Focal length in millimeters

# Camera resolution (assuming square pixels for simplicity)
image_width = 1280
image_height = 720

# Example camera height from the ground
camera_height = 300  # in units consistent with world coordinates
# get from pixhawk ^^

def get_random_bounding_box() -> np.array:
  '''
  For testing purposed only.
  Get list of four points within image resolution values that
  simulate a bounding box.

  Args: None
  Returns: list of lists of 2-dim coord. points
  '''
  x_vals = [image_width*rd.random(), image_width*rd.random()]   # create two random x-pixel-coords
  y_vals = [image_height*rd.random(), image_height*rd.random()] # create two random y-pixel-coords
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

def main():
  # Calculate focal lengths in pixels
  horizontal_focal_length_px = (image_width * focal_length_mm) / sensor_width_mm
  vertical_focal_length_px = (image_height * focal_length_mm) / sensor_width_mm

  # Principal point (assuming the image center)
  principal_point = (image_width / 2, image_height / 2)

  # Read in current gps point of aircraft
  #curr_gps = np.array([[30.3240575,-97.6037814]], dtype=np.float32) # dummy gps value for now
  curr_gps = tp.receive_telem() # not sure how to get this to work. causes import error of some kind

  # Read in bounding box value
  curr_bbox = bbox_data[len(bbox_data)]
  image_points = curr_bbox['Bbox']
  image_status = curr_bbox['Class']

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
  print("Aircraft GPS Coord.: ", curr_gps)
  print("Object GPS Estimation: ", curr_gps+world_points)
  print("Object Class: ", image_status)

if __name__ == '__main__':
  main()