from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv

# set happy and sad templates
templates = []
templates.append(cv.imread("happy.png", cv.IMREAD_GRAYSCALE))
templates.append(cv.imread("sad.png", cv.IMREAD_GRAYSCALE))

# get dimensions of templates
templateShapes = []
templateShapes.append(templates[0].shape[:: -1])
templateShapes.append(templates[1].shape[:: -1])

# dimensions for bounding box calculations
w = templateShapes[0][1]
h = templateShapes[0][0]

# methods of computation: which one do i use ;-;
method = cv.TM_CCOEFF_NORMED # decent for video, meh for image

# testing video
vid = cv.VideoCapture("testclip.mp4")  

"""
this function ...

    - takes in a video as input
    - performs template matching on each frame of the video
"""

def videoTemplateMatching(templates, vid, method, w, h):

    # how speecific template match is
    threshold = 0.8
    
    while(True):  

        # read video frame by frame
        ret, frame = vid.read()  
    
        # make each frame grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  
        
        # template matching for happy and sad facecs
        res1 = cv.matchTemplate(gray, templates[0], method)
        res2 = cv.matchTemplate(gray, templates[1], method)

        # store coordinates of matched area
        loc1 = np.where(res1 >= threshold) 
        loc2 = np.where(res2 >= threshold) 

        # only when a happy target is detected
        for pt in zip(*loc1[::-1]): 
                
                # add bounding box in matched area
                cv.rectangle(gray, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)        

        # only when a sad target is detected
        for pt in zip(*loc2[::-1]): 
                
                # add bounding box in matched area
                cv.rectangle(gray, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

        # display frames
        cv.imshow('frame', gray)  
        if cv.waitKey(1) & 0xFF == ord('q'):  
            break  
  
    # release capture when video ends
    vid.release()  
    cv.destroyAllWindows()  

if __name__ == "__main__":

    # call function
    videoTemplateMatching(templates, vid, method, w, h)

