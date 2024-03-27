import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import os
import psutil
import time

def load_and_train(directory):
    """
    Function to load and preprocess image data
    """
    X = []
    y = []
    for folder in os.listdir(directory):
        label = 1 if folder == 'happy' else 0
        for filename in os.listdir(os.path.join(directory, folder)):
            img = cv2.imread(os.path.join(directory, folder, filename), cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (64, 64))  # Resize image to 64x64
            X.append(img.flatten())  # Flatten image array
            y.append(label)

    # Train SVM classifier
    clf = SVC(kernel='linear')
    clf.fit(np.array(X), np.array(y))
    return clf

def detect_smiley(clf):
    # Define the parameters for circle detection
    dp = 1  # Inverse ratio of the accumulator resolution to the image resolution
    minDist = 100  # Minimum distance between the centers of detected circles
    param1 = 280  # Upper threshold for the internal Canny edge detector
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
        if circles is not None:
            circles = circles[0, :].astype("int")
            for (x, y, r) in circles:
                face_roi = gray[y:y+r, x:x+r]
                face_roi = cv2.resize(face_roi, (64, 64))  # Resize face region to 64x64
                face_flatten = face_roi.flatten()
                prediction = clf.predict([face_flatten])[0]
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

def measure_cpu_usage(duration):
    """
    Function to measure CPU usage
    """
    start_time = time.time()
    end_time = start_time + duration

    cpu_percentages = []
    while time.time() < end_time:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_percentages.append(cpu_percent)

    avg_cpu_usage = sum(cpu_percentages) / len(cpu_percentages)
    print("Average CPU Usage:", avg_cpu_usage)
    return avg_cpu_usage



if __name__ == "__main__":
    # train data and test accuracy
    clf = load_and_train('smiley_faces_dataset')

    # detect from live video feed
    detect_smiley(clf)

    # Measure CPU usage for 10 seconds
    avg_cpu_usage = measure_cpu_usage(10)