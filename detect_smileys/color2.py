import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Initialize the PiCamera
camera = PiCamera()
camera.resolution = (640, 480)  # Adjust the resolution as needed
camera.framerate = 32

# Allow the camera to warm up
time.sleep(0.1)

# Capture a video stream from the camera
rawCapture = PiRGBArray(camera, size=(640, 480))

# Wait for the automatic gain control to settle
time.sleep(2)

# OpenCV object for video capture
video_capture = cv2.VideoCapture()

# Open the video stream
video_capture.open(camera.capture_continuous(rawCapture, format="rgb", use_video_port=True))

# Main loop to capture and process frames
for frame in video_capture:
    # Extract the raw NumPy array representing the image
    image = frame.array
    
    # Perform any processing here (e.g., color correction)
    # corrected_image = correct_colors(image)
    
    # Display the frame
    cv2.imshow("Frame", image)
    
    # Clear the stream for the next frame
    rawCapture.truncate(0)
    
    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video stream and close OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
