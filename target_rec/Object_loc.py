import cv2
import numpy as np

# Camera sensor width in millimeters
sensor_width_mm = 4.712

# Focal length in millimeters
focal_length_mm = 16

# Camera resolution (assuming square pixels for simplicity)
image_width = 2048
image_height = 1520

# Calculate focal lengths in pixels
horizontal_focal_length_px = (image_width * focal_length_mm) / sensor_width_mm
vertical_focal_length_px = (image_height * focal_length_mm) / sensor_width_mm

# Principal point (assuming the image center)
principal_point = (image_width / 2, image_height / 2)

# Example points in the camera image
image_points = np.array([[10, 20], [50, 30], [80, 90]], dtype=np.float32)

# Camera matrix
camera_matrix = np.array([[horizontal_focal_length_px, 0, principal_point[0]],
                          [0, vertical_focal_length_px, principal_point[1]],
                          [0, 0, 1]])

# Example camera height from the ground
camera_height = 300  # in units consistent with world coordinates

# Define transformation matrix assuming the camera is pointing straight down
rotation_matrix = np.eye(3)
translation_vector = np.array([0, 0, camera_height])

# Combine rotation and translation into a single matrix
extrinsic_matrix = np.hstack((rotation_matrix, translation_vector.reshape(3, 1)))

# Perform perspective transformation
world_points = cv2.convertPointsToHomogeneous(image_points)
world_points = cv2.perspectiveTransform(world_points, np.linalg.inv(camera_matrix) @ extrinsic_matrix)

print("Object coordinates in world space:", world_points[:, 0, :])
