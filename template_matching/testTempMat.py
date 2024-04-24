import numpy as np
import cv2 as cv
import json

# set happy and sad templates
templates = []
templates.append(cv.imread("happy.png", cv.IMREAD_GRAYSCALE))
templates.append(cv.imread("sad.png", cv.IMREAD_GRAYSCALE))

# get dimensions of templates
templateShapes = []
templateShapes.append(templates[0].shape[:: -1])
templateShapes.append(templates[1].shape[:: -1])

# methods of computation: which one do i use ;-;
method = cv.TM_CCOEFF_NORMED # decent for video, meh for image

# testing video
# vid = cv.VideoCapture("testclip.mp4") 
vid = cv.VideoCapture(0)

"""
this function ...

    - takes in a video as input
    - performs template matching on each frame of the video
    - writes coordinates of bounding boxes to file
"""

def videoTemplateMatching(templates, vid, method):

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

            # dimensions for bounding box calculations
            w = templateShapes[0][1]
            h = templateShapes[0][0]
                
            # add bounding box in matched area
            cv.rectangle(gray, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)

            # top left corner point
            top_left = pt

            # bottom right corner point
            bottom_right = (pt[0] + w, pt[1] + h)

            # data for json file
            dictionary = {
                "top_left": top_left,
                "top_right": (bottom_right[0], top_left[1]),
                "bottom_left": (top_left[0], bottom_right[1]),
                "bottom_right": bottom_right
            }
            
            # serializing json
            json_object = json.dumps(dictionary, indent=4, default=str)

            # write to json file
            with open("happycoordinates.json", "w") as outfile:
                outfile.write(json_object)

        # only when a sad target is detected
        for pt in zip(*loc2[::-1]): 

            # dimensions for bounding box calculations
            w = templateShapes[1][1]
            h = templateShapes[1][0]
                
            # add bounding box in matched area
            cv.rectangle(gray, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

            # top left corner point
            top_left = pt

            # bottom right corner point
            bottom_right = (pt[0] + w, pt[1] + h)

            # data for json file
            dictionary = {
                "top_left": top_left,
                "top_right": (bottom_right[0], top_left[1]),
                "bottom_left": (top_left[0], bottom_right[1]),
                "bottom_right": bottom_right
            }
            
            # serializing json
            json_object = json.dumps(dictionary, indent=4, default=str)

            # write to json file
            with open("sadcoordinates.json", "w") as outfile:
                outfile.write(json_object)

        # display frames
        cv.imshow('frame', gray)  
        if cv.waitKey(1) & 0xFF == ord('q'):  
            break  
  
    # release capture when video ends
    vid.release()  
    cv.destroyAllWindows()  

if __name__ == "__main__":

    # call function
    videoTemplateMatching(templates, vid, method)

