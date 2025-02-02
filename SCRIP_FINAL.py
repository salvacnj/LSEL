#!/usr/bin/python


import io
import random
import picamera
import fractions
import RPi.GPIO as GPIO
import subprocess
import threading
import time
import pygame
import random
import os
import sys
from sense_hat import SenseHat


# SENSE HAT
OFFSET_LEFT = 1
OFFSET_TOP = 2

NUMS =[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,  # 0
       0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,  # 1
       1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,  # 2
       1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,  # 3
       1,0,0,1,0,1,1,1,1,0,0,1,0,0,1,  # 4
       1,1,1,1,0,0,1,1,1,0,0,1,1,1,1,  # 5
       1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,  # 6
       1,1,1,0,0,1,0,1,0,1,0,0,1,0,0,  # 7
       1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,  # 8
       1,1,1,1,0,1,1,1,1,0,0,1,0,0,1]  # 9


# VIDEO BUFFER PARAMETERS
VIDEO_BEFORE = 3 
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
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# BALL DETECTED VARIABLE
ball = 0

# CHISPAS ON
chispas_on = 0



# Displays a single digit (0-9)
def show_digit(val, xd, yd, r, g, b):
  offset = val * 15
  for p in range(offset, offset + 15):
    xt = p % 3
    yt = (p-offset) // 3
    sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

# Displays a two-digits positive number (0-99)
def show_number(val, r, g, b):
  abs_val = abs(val)
  tens = abs_val // 10
  units = abs_val % 10
  if (abs_val > 9): show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
  show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)


# PRINT THE SCORE STATUS
def print_marcador():
    subprocess.call(["clear"])
    print("------------------------------------------------")
    print("                  SCORE                         ")
    print("------------------------------------------------")
    print("    P1: "+str(marcador_1)+"   P2: "+str(marcador_2))
    print("------------------------------------------------")

    sense.clear()
    show_number(marcador_1, 200, 0, 60)


def chispas():
  sense.show_message("I-ANASTA")
  contador = 0
  activo = 1

  while activo:
    if contador < 100:
      contador = contador +1
      x = random.randint(0, 7)
      y = random.randint(0, 7)
      r = random.randint(0, 255)
      g = random.randint(0, 255)
      b = random.randint(0, 255)
      sense.set_pixel(x, y, r, g, b)
      time.sleep(0.01)
    else:
      activo=0
      sense.show_message("SELECT GAME")
      sense.clear()

    



# VIENVENIDA MENSAJE
def initial_mesaje():
    global game_selected
    global marcador_1
    global marcador_2


    marcador_1 = 0
    marcador_2 = 0


    chispas_process = threading.Thread(target=chispas)
    chispas_process.start()

    
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

    audio_c = threading.Thread(target=reproducir_comienzo)
    audio_c.start()
    time.sleep(9)
    print_marcador()





# DETECTION OF RISING EVENT IN THE PIN
def interruption (channel):
        global ball
        ball = 1

GPIO.add_event_detect(26, GPIO.RISING, callback = interruption)




def reproducir_comienzo():
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


def reproducir_fondo():
    print("REPRODUCTION")

    while True:
        pygame.mixer.music.load("fondo_1.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
        time.sleep(190)

        pygame.mixer.music.load("fondo_2.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
        time.sleep(245)

        pygame.mixer.music.load("fondo_3.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
        time.sleep(220)

        pygame.mixer.music.load("fondo_4.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
        time.sleep(290)

        pygame.mixer.music.load("fondo_5.wav")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play()
        time.sleep(390)


def reproducir_final():
    print("FINAL MATCH")


# AUDIO REPRODUCTION FOR GOAL
def reproducir_audio():
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
        subprocess.call(["rm","motion.mp4"])
        subprocess.call(["MP4Box","-fps","30","-add","motion.h264","motion.mp4"])
        subprocess.call(["omxplayer","motion.mp4"])


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
        pygame.mixer.init()

        # SENSE HAT INIT
        sense = SenseHat()
        sense.clear()

        audio_fondo = threading.Thread(target=reproducir_fondo)
        audio_fondo.start()

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
                            print_marcador()

                            if (marcador_1 > 21):
                                print_marcador()
                                print("CONGRATULATIONS!!! -> PLAYER 1 WINS !!")

                                # WE SHOW LAST GOAL
                                repeticion = threading.Thread(target=mostrar_video)
                                audio_f = threading.Thread(target=reproducir_final)
                                repeticion.start()
                                audio_f.start()
                                time.sleep(15)
                                reboot_script = 1
                                break
                                


                            elif (marcador_2 >21):
                                print_marcador()
                                print("CONGRATULATIONS!!! -> PLAYER 2 WINS !!")

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

                            # SHOW SCORE
                            print_marcador()

                            #ESPERAMOS PARA VOLVER A DETECTAR
                            time.sleep(TIME_BETWEEN_POINTS)

                            ball = 0
                                         


                            
                        elif game_selected == 2:

                            #leer player ID desde socket
                            actualiza_marcador(player_id,2)
                            subprocess.call(["clear"])
                            print_marcador()


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
                pygame.quit()
                sense.clear()
                sys.exit(1)