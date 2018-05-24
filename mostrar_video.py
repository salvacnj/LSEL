
import subprocess

subprocess.call(["rm","motion.mp4"])
subprocess.call(["MP4Box","-fps","30","-add","motion.h264","motion.mp4"])
subprocess.call(["omxplayer","motion.mp4"])