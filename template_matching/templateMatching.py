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
# method = cv.TM_CCOEFF # bad for video, okay for image
method = cv.TM_CCOEFF_NORMED # decent for video, bad for image
# method = cv.TM_CCORR # doesnt always have box, but cant find target
# method = cv.TM_CCORR_NORMED # about as accurate as cv.TM_CCOEFF_NORMED
# method = cv.TM_SQDIFF # needs masking
# method = cv.TM_SQDIFF_NORMED # needs masking

# testing image
img = cv.imread("testhappy.png", cv.IMREAD_GRAYSCALE)

# testing video
vid = cv.VideoCapture("testclip.mp4")  

"""
this function ...

    - takes in an image as input
    - performs template matching on the image for each template
"""

def templateMatching(templates, img, w, h):

    for i in templates:

        # do template matching
        res = cv.matchTemplate(img, i, method)

        # store coordinates of matched area
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        # calculate coordinates
        # top_left = min_loc # for SQDIFF methods
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # add bounding box
        cv.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)

        # view image
        plt.imshow(img)
        plt.show()

"""
this function ...

    - takes in a video as input
    - performs template matching on each frame of the video
"""

def videoTemplateMatching(templates, vid, w, h):
    
    while(True):  

        # read video frame by frame
        ret, frame = vid.read()  
    
        # make each frame grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  

        # do template matching
        res = cv.matchTemplate(gray, templates[0], method)

        # treshold for 
        threshold = 0.8
        
        # store coordinates of matched area
        loc = np.where(res >= threshold) 

        # add bounding box in matched area
        for pt in zip(*loc[::-1]): 
            cv.rectangle(gray, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2) 

        # display frames
        cv.imshow('frame', gray)  
        if cv.waitKey(1) & 0xFF == ord('q'):  
            break  
  
    # release capture when video ends
    vid.release()  
    cv.destroyAllWindows()  

if __name__ == "__main__":
    # templateMatching(templates, img, w, h)
    videoTemplateMatching(templates, vid, w, h)

