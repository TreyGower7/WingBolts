import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import os
import psutil
import time
from matplotlib import pyplot as plt
# print(os.path.dirname('psutil').__file__)
import site
print(site.getsitepackages())


import tensorflow as tf

model = tf.keras.models.load_model("models/cnn_first.keras")


def detect_smiley():
    # Define the parameters for circle detection
    dp = 1  # Inverse ratio of the accumulator resolution to the image resolution
    minDist = 100  # Minimum distance between the centers of detected circles
    param1 = 350  # Upper threshold for the internal Canny edge detector
    param2 = 35   # Threshold for center detection
    minRadius = 5  # Minimum radius to be detected
    maxRadius = 100  # Maximum radius to be detected
    
    # Start video capture
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect circles in the frame
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
       
        # For each detected face, classify it as happy or sad
        for (x, y, r) in circles:
                face_roi = gray[y:y+r, x:x+r]
                face_roi = cv2.resize(face_roi, (64, 64))  # Resize face region to 64x64
                
                # Preprocess the image for the model
                face_array = np.expand_dims(face_roi, axis=0)  # Add batch dimension
                face_array = face_array / 255.0  # Normalize pixel values
                
                # Predict using the TensorFlow model
                probabilities = model.predict(face_array)[0]
                
                # Check if the confidence for either class is above the threshold
                threshold = 0.7  # Adjust this threshold as needed
                if max(probabilities) >= threshold:
                    prediction = np.argmax(probabilities)
                    label = "Happy" if prediction == 1 else "Sad"
                    color = (0, 255, 0) if prediction == 1 else (0, 0, 255)
                    cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Display the frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

def main():
    detect_smiley()

if __name__ == "__main__":
    main()