# RESIZES BIG IMAGES TO SMALL

import os
import cv2


def resize_images_in_directory(input_dir, output_dir, target_size):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        print("path not there")
    # Get a list of all files in the input directory
    files = os.listdir(input_dir)
    
    # Loop through each file in the input directory
    for file in files:
        # Check if the file is an image (assuming common image extensions)
            # Read the image
            image_path = os.path.join(input_dir, file)
            image = cv2.imread(image_path)

            # Resize the image
            resized_image = cv2.resize(image, (107, 143))

            # Write the resized image to the output directory
            output_path = os.path.join(output_dir, file)
            cv2.imwrite(output_path, resized_image)
            print(image_path)

# Example usage:
input_dir = 'big_smiley_faces_dataset/sad'
output_dir = 'smiley_faces_dataset/sad'
target_size = (5712/10, 4284/10)  # Specify the target size as (width, height)

resize_images_in_directory(input_dir, output_dir, target_size)