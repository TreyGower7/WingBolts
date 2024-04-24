import cv2
from picamera2 import Picamera2

camera = Picamera2()
camera.preview_configuration.main.size=(1280,720)
camera.preview_configuration.main.format='BGR888'
camera.preview_configuration.align()
camera.configure('preview')
camera.start()

while True:
    frame = camera.capture_array()
    cv2.imshow('camera', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
