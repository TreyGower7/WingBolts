# object detection
tflite model and scripts to run 

need to pull:  
`custom_model_lite`
`tflite_webcam_bboxes.py`

```
# webcam
python tflite_webcam_bboxes.py --modeldir=custom_model_lite
# input vid
python3 tflite_video_bboxes.py --modeldir=custom_model_lite --video='flight_footage.mp4' 
```
outputs to read (for gps coords):  
`webcam_bbox_log.txt`

https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi
