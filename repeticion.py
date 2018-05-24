import io
import random
import picamera
import fractions
import RPi.GPIO as GPIO
import subprocess
import threading
import time


# VIDEO BUFFER PARAMETERS
VIDEO_BEFORE = 2 
VIDEO_AFTER = 2

# INTERRUP PIN CONFIGURATION
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

# BALL DETECTED VARIABLE
ball = 0


# DETECTION OF RISING EVENT IN THE PIN
def interruption (channel):
        global ball
        ball = 1

GPIO.add_event_detect(23, GPIO.RISING, callback = interruption)


# SHOW REPETITION
def mostrar_video():
        camera.wait_recording(VIDEO_AFTER)
        write_video(stream)
        print('[CAM-STATE]: SHOWING VIDEO')
        print("[STATE]: MOSTRANDO REPETICION")
        subprocess.call(["rm","motion.mp4"])
        subprocess.call(["MP4Box","-fps","30","-add","motion.h264","motion.mp4"])
        subprocess.call(["omxplayer","motion.mp4"])
        print("[STATE]: REPETICION MOSTRADA")

# MODIFY BUFFER TO ADD
def write_video(stream):
        with stream.lock:
                for frame in stream.frames:
                        if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                                stream.seek(frame.position)
                                break
                with io.open('motion.h264','wb') as output:
                        output.write(stream.read())

# MAIN LOPP
with picamera.PiCamera() as camera:

        # TEXT TO SHOW IN THE REPETITION
        camera.annotate_text = "REPETICION"        
        camera.annotate_text_size = 160
        camera.annotate_background = picamera.Color('black')

        # CIRCULAR BUFFER SET-UP
        stream = picamera.PiCameraCircularIO(camera, seconds=VIDEO_BEFORE)
        camera.start_recording(stream, format='h264')

        

        try:
                print('[CAM-STATE]: Waiting BALL')
                while True:
                        camera.wait_recording(1)

                        if ball == 1:

                                print("Ball detected...")
                                # THREADS DEFINITIONS
                                repeticion = threading.Thread(target=mostrar_video)


 
                               # THREADS EJECUTION
                                repeticion.start()

                                #ESPERAMOS PARA VOLVER A DETECTAR
                                time.sleep(2)

                                ball = 0
                                print('[CAM-STATE]: Waiting BALL')

                                

        finally:
                camera.stop_recording()