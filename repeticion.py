import io
import random
import picamera
import fractions
import RPi.GPIO as GPIO
import subprocess
import threading
import time
import pygame.mixer
import random


# VIDEO BUFFER PARAMETERS
VIDEO_BEFORE = 2 
VIDEO_AFTER = 1

# PLAYERS SCORE
docker_1 = 0
docker_2 = 0
marcador_1 = 0
marcador_2 = 0

# GAME SELECTION
game_selected = 0

# INTERRUP PIN CONFIGURATION
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

# BALL DETECTED VARIABLE
ball = 0

# VIENVENIDA MENSAJE
def initial_mesaje():
    global game_selected

    print("--------------------------------------------------------")
    print("                                                        ")
    print("     |||      ||  |||||||||        ||||                 ")
    print("     ||||     ||  ||||   |||     |||||||| ")
    print("     || ||    ||  ||||   |||   ||||   |||| ")
    print("     ||  ||   ||  |||||||||    ||||   |||| ")
    print("     ||   ||  ||  |||||||||    ||||||||||| ")
    print("     ||    || ||  ||||   |||   ||||   |||| ")
    print("     ||     ||||  ||||   |||   ||||   |||| ")
    print("     ||      |||  |||||||||    ||||   |||| ")
    print("                                                        ")
    print(" -- ----------------------------------------------------")
    print("          SELECT THE NAME OF YOUR GAME                  ")
    print("  1 ->  21 GAME:                                        ")
    print("        The first player who achive 21 points wins      ")
    print("                                                        ")
    print("  2 ->  1 vs 1 SCORE:                                   ")
    print("        Batlle beetween two player! There is no limits  ")
    print("        score                                           ")
    print("--------------------------------------------------------")
    print("  MAKE YOUR CHOICE:                                     ")
    game_selected = input()

    while (game_selected != 1 and game_selected != 2):
        print("--------------------------------------------------------")
        print("  WRONG SLECTION, MAKE YOUR CHOICE AGAIN:               ")
        game_selected = input()
    

    if game_selected == 1:
        print("--------------------------------------------------------")
        print("  21 GAME SELECTED, GOOD LUCK:                          ")
    elif game_selected == 2: 
        print("--------------------------------------------------------")
        print("  1 vs 1 SELECTED, GOOD LUCK:                           ")




# DETECTION OF RISING EVENT IN THE PIN
def interruption (channel):
        global ball
        ball = 1

GPIO.add_event_detect(23, GPIO.RISING, callback = interruption)


# REPRODUCE AUDIO
def reproducir_audio():
        print("[STATE]: REPRODUCIENDO AUDIO")
        num=random.randrange(4)

        switcher1 = {
                0: pygame.mixer.Sound("1.wav"),
                1: pygame.mixer.Sound("2.wav"),
                2: pygame.mixer.Sound("3.wav"),
                3: pygame.mixer.Sound("4.wav")
        }
        switcher2 = {
                0: 7,
                1: 5,
                2: 3,
                3: 4
        }
        sonido = switcher1.get(num,pygame.mixer.Sound("4.wav"))
        dormir = switcher2.get(num)
        sonido.play()
        time.sleep(dormir)


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


# UPDATE SCORE PLAYER 1/2 
def actualiza_marcador(player, points):
    if player == 1:
        marcador_1 = marcador_1 + points
    else:
        marcador_2 = marcador_2 + points

# MAIN LOPP
with picamera.PiCamera() as camera:

        # TEXT TO SHOW IN THE REPETITION
        camera.annotate_text = "REPETICION"        
        camera.annotate_text_size = 160
        camera.annotate_background = picamera.Color('black')

        # CIRCULAR BUFFER SET-UP
        stream = picamera.PiCameraCircularIO(camera, seconds=VIDEO_BEFORE)
        camera.start_recording(stream, format='h264')

        # AUDIO INITIALICE
        pygame.mixer.init(44100, 16, 2, 4096)

        initial_mesaje()      

        try:
                while True:

                        camera.wait_recording(1)

                        if ball == 1:
                            if game_selected == 1:
                                print("Ball detected 1...")

                                # THREADS DEFINITIONS
                                repeticion = threading.Thread(target=mostrar_video)
                                audio = threading.Thread(target=reproducir_audio)

                                # THREADS EJECUTION
                                repeticion.start()
                                audio.start()

                                #ESPERAMOS PARA VOLVER A DETECTAR
                                time.sleep(2)

                                ball = 0
                                print('[CAM-STATE]: Waiting BALL')             


                                
                            elif game_selected == 2:
                                print("Ball detected 2...")

                                # THREADS DEFINITIONS
                                repeticion = threading.Thread(target=mostrar_video)
                                audio = threading.Thread(target=reproducir_audio)

                                # THREADS EJECUTION
                                repeticion.start()
                                audio.start()

                                #ESPERAMOS PARA VOLVER A DETECTAR
                                time.sleep(2)

                                ball = 0
                                print('[CAM-STATE]: Waiting BALL')  
                                

                                                            

        finally:
                camera.stop_recording()