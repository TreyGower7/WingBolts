import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
  _, frame = cap.read()

  cv2.imshow('Frame', frame)

  key = cv2.watiKey(1)

cap.release()
cv2.destroyAllWindows()
