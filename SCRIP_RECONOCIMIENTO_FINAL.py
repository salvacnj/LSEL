#python color_tracking.py --video balls.mp4
#python color_tracking.py
 
# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import urllib #for reading image from URL
from sense_hat import SenseHat
 
number = [
0,1,1,1, # Zero
0,1,0,1,
0,1,0,1,
0,1,1,1,
0,0,1,0, # One
0,1,1,0,
0,0,1,0,
0,1,1,1,
0,1,1,1, # Two
0,0,1,1,
0,1,1,0,
0,1,1,1,
0,1,1,1, # Three
0,0,1,1,
0,0,1,1,
0,1,1,1,
0,1,0,1, # Four
0,1,1,1,
0,0,0,1,
0,0,0,1,
0,1,1,1, # Five
0,1,1,0,
0,0,1,1,
0,1,1,1,
0,1,0,0, # Six
0,1,1,1,
0,1,0,1,
0,1,1,1,
0,1,1,1, # Seven
0,0,0,1,
0,0,1,0,
0,1,0,0,
0,1,1,1, # Eight
0,1,1,1,
0,1,1,1,
0,1,1,1,
0,1,1,1, # Nine
0,1,0,1,
0,1,1,1,
0,0,0,1
]

player1_color = [255,0,0] # Red
player2_color = [0,255,255] # Cyan
empty = [0,0,0] # Black
player1_puntos = 0
player2_puntos = 0
scoreboard_image = [
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0
]

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
 
# define the lower and upper boundaries of the colors in the HSV color space
#lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)} #assign new item lower['blue'] = (93, 10, 0)
#upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}

lower = {'greenblue':(151,157,106),'purple':(51,28,37)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'greenblue':(249,235,170),'purple':(203,57,983)}

#azul verdoso player 1:
#rgb=0,203,95

#morado player 2:
#hsv=304,81,39
#en foto
#rgb=66,47,87

#ULTIMA ACTUALIZACION
#lower = {'greenblue':(151,157,106),'purple':(48,28,35)} #assign new item lower['blue'] = (93, 10, 0)
#upper = {'greenblue':(249,235,170),'purple':(203,58,123)}


#bgr!!!
 
# define standard colors for circle around the object
colors = {'greenblue':(223,210,156),'purple':(96,33,53)}
 
#pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
#if not args.get("video", False):
    #camera = cv2.VideoCapture(0)
   
 
# otherwise, grab a reference to the video file
#else:
#    camera = cv2.VideoCapture(args["video"])
# keep looping
#camera = cv2.VideoCapture(0)
camera=WebcamVideoStream(src=0).start()
fps = FPS().start()

i=0

#troncho de la prueba

#####

while True:
    # grab the current frame
    #(grabbed, frame) = camera.read()
    frame=camera.read()
    
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    #IP webcam image stream
    #URL = 'http://10.254.254.102:8080/shot.jpg'
    #urllib.urlretrieve(URL, 'shot1.jpg')
    #frame = cv2.imread('shot1.jpg')
 
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    #camera.set(cv2.CV_CAP_PROP_FPS, 30)
    frame = imutils.resize(frame, width=300)
 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(blurred, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
               
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
       
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
       
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 50 and radius < 170:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame,key + " ball", (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
                print("-------------")
                print(i)
                print(radius)
                print("Hay bola")
                print(key)
                i=i+1
 
     
    # show the frame to our screen
    #i=i+1
    cv2.imshow("Frame", frame)
    #cv2.imshow("Blurred", mask)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
