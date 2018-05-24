import io
import random
import picamera
import fractions
import RPi.GPIO as GPIO
import subprocess



VIDEO_TOTAL = 10
VIDEO_AFTER = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

ball = 0

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
                with io.open('motion.h264','wb') as output:
                        output.write(stream.read())

with picamera.PiCamera() as camera:
        camera.annotate_text = "REPETICION"        
        camera.annotate_text_size = 160
        stream = picamera.PiCameraCircularIO(camera, seconds=VIDEO_TOTAL)
        camera.start_recording(stream, format='h264')

        try:
                print('[CAM-STATE]: Waiting BALL')
                while True:
                        camera.wait_recording(1)

                        if ball == 1:
                                print('[CAM-STATE]: BALL DETECTED')
                                camera.wait_recording(VIDEO_AFTER)
                                write_video(stream)
                                print('[CAM-STATE]: SHOWING VIDEO')

                                #BUSCAR PARA EJECUTAR COMANDO EN OTRA SHELL
                                subprocess.call(["python","mostrar_video.py"])
          
                                print('[CAM-STATE]: CONTINUE')
                                break;
                                ball = 0

                                

        finally:
                camera.stop_recording()