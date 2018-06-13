#!/usr/bin/python


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
import os
import sys


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

# PLAYER IDENTIFICATION
player_id = 1

# INTERRUP PIN CONFIGURATION
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)


# BALL DETECTED VARIABLE
ball = 0



# VIENVENIDA MENSAJE
def initial_mesaje():
    global game_selected
    global marcador_1
    global marcador_2

    marcador_1 = 0
    marcador_2 = 0


    subprocess.call(["clear"])
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



def reproducir_final():
    print("FINAL MATCH")


# AUDIO REPRODUCTION FOR GOAL
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
    global marcador_1
    global marcador_2

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

                                #leer player ID desde socket

                                actualiza_marcador(player_id,2)
                                subprocess.call(["clear"])
                                print("------------------------------------------------")
                                print("    P1: "+str(marcador_1)+"   P2: "+str(marcador_2))
                                print("------------------------------------------------")

                                if (marcador_1 > 21):
                                    subprocess.call(["clear"])
                                    print("PLAYER 1 WINS!")
                                    print("------------------------------------------------")
                                    print("    P1: "+str(marcador_1)+"   P2: "+str(marcador_2))
                                    print("------------------------------------------------")

                                    # WE SHOW LAST GOAL
                                    repeticion = threading.Thread(target=mostrar_video)
                                    audio_f = threading.Thread(target=reproducir_final)
                                    repeticion.start()
                                    audio_f.start()
                                    time.sleep(5)
                                    # REINICIAR SCRIPT
                                    


                                elif (marcador_2 >21):
                                    subprocess.call(["clear"])
                                    print("PLAYER 2 WINS!")
                                    print("------------------------------------------------")
                                    print("    P1: "+str(marcador_1)+"   P2: "+str(marcador_2))
                                    print("------------------------------------------------")

                                    # WE SHOW LAST GOAL
                                    repeticion = threading.Thread(target=mostrar_video)
                                    audio_f = threading.Thread(target=reproducir_final)
                                    repeticion.start()
                                    audio_f.start()
                                    initial_mesaje()
                                    time.sleep(5)
                                    os.execl('/home/pi/VIDEO_SALVA/LSEL/repeticion.py',[''])

                                # SHOW REPETITIOM ALEATORY
                                if random.randrange(10) > 6:
                                    repeticion = threading.Thread(target=mostrar_video)
                                    repeticion.start()


                                # THREADS DEFINITIONS
                                audio = threading.Thread(target=reproducir_audio)

                                # THREADS EJECUTION 
                                audio.start()

                                subprocess.call(["clear"])
                                print("------------------------------------------------")
                                print("    P1: "+str(marcador_1)+"   P2: "+str(marcador_2))
                                print("------------------------------------------------")

                                #ESPERAMOS PARA VOLVER A DETECTAR
                                time.sleep(2)

                                ball = 0
                                             


                                
                            elif game_selected == 2:

                                #leer player ID desde socket
                                actualiza_marcador(player_id,2)
                                subprocess.call(["clear"])
                                print("------------------------------------------------")
                                print("    P1: "+str(marcador_1)+"   P2: "+str(marcador_2))
                                print("------------------------------------------------")


                                                                # SHOW REPETITIOM ALEATORY
                                if random.randrange(10) > 6:
                                    repeticion = threading.Thread(target=mostrar_video)
                                    repeticion.start()

                                # THREADS DEFINITIONS
                                audio = threading.Thread(target=reproducir_audio)

                                # THREADS EJECUTION
                                audio.start()

                                #ESPERAMOS PARA VOLVER A DETECTAR
                                time.sleep(2)

                                ball = 0
                            
                                                            

        finally:
                camera.stop_recording()