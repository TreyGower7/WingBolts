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

# method of computation
method = cv.TM_CCOEFF_NORMED
# method = cv.TM_CCOEFF
# method = cv.TM_CCORR_NORMED 

# testing image
img = cv.imread("testhappy.png", cv.IMREAD_GRAYSCALE)
# img = cv.imread("notarget.png", cv.IMREAD_GRAYSCALE)
# img = cv.imread("happy.png", cv.IMREAD_GRAYSCALE)

# testing video
cap = cv.VideoCapture("testclip.mp4")  

"""
this function ... 

    - takes in an image as input
    - tests the OpenCV HoughCircles() function: searches for a circle in an image
"""

def searchCircle(img):

    # Blur using 3 * 3 kernel. 
    blurredimg = cv.blur(img, (3, 3)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv.HoughCircles(blurredimg,  
                    cv.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                param2 = 30, minRadius = 0, maxRadius = 0) 
    
    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv.circle(img, (a, b), r, (255, 0, 0), 2) 

    # view image
    plt.imshow(img)
    plt.show()

"""
this function ...

    - takes in an image as input
    - performs template matching on the image for each template
"""

def templateMatching(img):

    for i in templates:

        # size of templates
        w = templateShapes[0][1]
        h = templateShapes[0][0]

        # do template matching
        res = cv.matchTemplate(img, i, method)

        # store coordinates of matched area
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        # calculate coordinates
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

def testVideo():

    # # video input
    # cap = cv.VideoCapture("testclip.mp4")  

    template = cv.imread("happy.png", cv.IMREAD_GRAYSCALE)

    w = templateShapes[0][1]
    h = templateShapes[0][0]
    
    while(True):  

        # read video frame by frame
        ret, frame = cap.read()  
    
        # make each frame grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  

        # do template matching
        res = cv.matchTemplate(gray, template, method)

        # store coordinates of matched area
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        # calculate coordinates
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        if res is not None:
        
            # add bounding box
            cv.rectangle(gray, top_left, bottom_right, (255, 0, 0), 2)
    
        # display frames
        cv.imshow('frame', gray)  
        if cv.waitKey(1) & 0xFF == ord('q'):  
            break  
  
    # release capture when video ends
    cap.release()  
    cv.destroyAllWindows()  

if __name__ == "__main__":
    # templateMatching(img)
    # searchCircle(img)
    testVideo()

