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

# TIME BETWEEN POINTS
TIME_BETWEEN_POINTS = 2

# PLAYERS SCORE
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

    audio_c = threading.Thread(target=reproducir_comienzo)
    audio_c.start()

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
    print("  MAKE YOUR CHOICE: ")
    game_selected = input()
    

    while (game_selected != 1 and game_selected != 2):
        print("--------------------------------------------------------")
        print("  WRONG SLECTION, MAKE YOUR CHOICE AGAIN: ")
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



def reproducir_comienzo():
    print("[STATE]: REPRODUCIENDO AUDIO COMIENZO")
    num=random.randrange(2)

    switcher1 = {
            0: pygame.mixer.Sound("Comienzo1.wav"),
            1: pygame.mixer.Sound("comienzo2.wav")
    }
    switcher2 = {
            0: 9,
            1: 8
    }

    sonido = switcher1.get(num,pygame.mixer.Sound("Comienzo1.wav"))
    dormir = switcher2.get(num)
    sonido.play()
    time.sleep(dormir)



def reproducir_final():
    print("FINAL MATCH")


# AUDIO REPRODUCTION FOR GOAL
def reproducir_audio():
        print("[STATE]: REPRODUCIENDO AUDIO")
        num=random.randrange(20)

        switcher1 = {
                0: pygame.mixer.Sound("1.wav"),
                1: pygame.mixer.Sound("2.wav"),
                2: pygame.mixer.Sound("3.wav"),
                3: pygame.mixer.Sound("4.wav"),
                4: pygame.mixer.Sound("5.wav"),
                5: pygame.mixer.Sound("6.wav"),
                6: pygame.mixer.Sound("7.wav"),
                7: pygame.mixer.Sound("8.wav"),
                8: pygame.mixer.Sound("9.wav"),
                9: pygame.mixer.Sound("10.wav"),
                10: pygame.mixer.Sound("11.wav"),
                11: pygame.mixer.Sound("12.wav"),
                12: pygame.mixer.Sound("13.wav"),
                13: pygame.mixer.Sound("14.wav"),
                14: pygame.mixer.Sound("15.wav"),
                15: pygame.mixer.Sound("16.wav"),
                16: pygame.mixer.Sound("17.wav"),
                17: pygame.mixer.Sound("18.wav"),
                18: pygame.mixer.Sound("19.wav"),
                19: pygame.mixer.Sound("20.wav"),
                20: pygame.mixer.Sound("21.wav")
        }
        switcher2 = {
                0: 7,
                1: 5,
                2: 3,
                3: 5,
                4: 4,
                5: 7,
                6: 7,
                7: 6,
                8: 10,
                9: 6,
                10: 12,
                11: 5,
                12: 8,
                13: 10,
                14: 7,
                15: 9,
                16: 4,
                17: 5,
                18: 10,
                19: 9,
                20: 10
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

        try:

            while True:

                reboot_script = 0

                initial_mesaje()      

                
                while reboot_script == 0:

                    camera.wait_recording(1)

                    if ball == 1:
                        if game_selected == 1:

                            #leer player ID desde socket

                            actualiza_marcador(player_id,2)
                            subprocess.call(["clear"])
                            print("------------------------------------------------")
                            print("    P1: "+str(marcador_1)+"   P2: "+str(marcador_2))
                            print("------------------------------------------------")

                            if (marcador_1 > 2):
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
                                time.sleep(15)
                                reboot_script = 1
                                break
                                


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
                                time.sleep(15)
                                reboot_script = 1
                                break

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
                            time.sleep(TIME_BETWEEN_POINTS)

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
                            time.sleep(TIME_BETWEEN_POINTS)

                            ball = 0
                                
                                                                    

        finally:
                camera.stop_recording()