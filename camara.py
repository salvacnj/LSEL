import io
import random
import picamera
import fractions
import RPi.GPIO as GPIO
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import os



VIDEO_TOTAL = 10
VIDEO_AFTER = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

ball = 0

b=10
g=60
r=255

# convert the target color to HSV orange
target_color = np.uint8([[[b, g, r]]])
target_color_hsv = cv2.cvtColor(target_color, cv2.COLOR_BGR2HSV)

#convert the target color to HSV green

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# boundaries for Hue define the proper color boundaries, saturation and values can vary a lot
target_color_h = target_color_hsv[0,0,0]
tolerance = 3
lower_hsv = np.array([max(0, target_color_h - tolerance), 150, 50])
upper_hsv = np.array([min(179, target_color_h + tolerance), 250, 250])




Jugador1 = 0
Jugador2 = 0


def interruption (channel):
        global ball
        ball = 1

GPIO.add_event_detect(23, GPIO.RISING, callback = interruption)



def write_video(stream):
        print('Writing video!')

        with stream.lock:
                for frame in stream.frames:
                        if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                                stream.seek(frame.position)
                                break
                with io.open('motion.mjpeg','wb') as output:
                        output.write(stream.read())


def detect_player():
        camera1 = cv2.VideoCapture("motion.mjpeg")
        (grabbed, frame) = camera1.read()
        frame = imutils.resize(frame, width=600)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask1 = cv2.inRange(hsv, lower_hsv, upper_hsv)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations =2)
        mask1 = cv2.erode(mask1, None, iterations=2)
        mask1 = cv2.dilate(mask1, None, iterations =2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cntsorange = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        font = cv2.FONT_HERSHEY_SIMPLEX
        (height,width,d) = frame.shape 

        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size
                if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)

                        if (center[0] > int(width/3) and center[0] < int((width/3)*2)):
                                if (center[1]> int(height/3) and center[1]< int((height/3)*2)):
                                        cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 5)
                                        cv2.putText(frame, 'Jugador2', (25,25), font, 0.5, (0,0,0), 1)
                        #Jugador2 = 1
                                else:
                                        cv2.putText(frame, 'Nada', (25,25), font, 0.5, (0,0,0), 1)
                        #Jugador2 = 0
                        else:
                                cv2.putText(frame, 'Nada', (25,25), font, 0.5, (0,0,0), 1)
                                Jugador2 = 0


with picamera.PiCamera() as camera:

  
        camera.annotate_text = "REPETICION"
        camera.annotate_text_size = 160

        stream = picamera.PiCameraCircularIO(camera, seconds=VIDEO_TOTAL)

        camera.start_recording(stream, format='mjpeg')

        try:
                print('Waiting ball')
                while True:
                        camera.wait_recording(1)

                        if ball == 1:
                                ball = 0
                                print('BALL DETECTED')
                                camera.wait_recording(VIDEO_AFTER)
                                write_video(stream)
                                print('VIDEO WRITE')

                                

        finally:
                camera.stop_recording()