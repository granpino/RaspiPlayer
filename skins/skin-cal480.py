#!/usr/bin/python
# pi-radio rev. 1.0
# This is to be used with a 3.5" HDMI touchscreen
# Tested with the Raspberry pi 2 and raspbian stretch
# The program must be run within the Lxterminal or the 
# touchscreen will be upside down
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import os
import glob
import random

pygame.init()

#define colors
cyan = 50, 255, 255
blue = 26, 0, 255
black = 0, 0, 0
white = 255, 235, 235
red = 255, 0, 0
green = 0, 255, 0

#other
os.system("mount /dev/sda1 /mnt/usbdrive") #setup for USB drive if used
subprocess.call("mpc random off", shell=True)
subprocess.call("mpc clear", shell=True)
subprocess.call("mpc volume 65", shell=True)
subprocess.call("mpc update ", shell=True)
subprocess.call("mpc load playlist", shell=True)
global mp3
mp3 = 0
shuffle = False

#_image = ('200x170.png','200x170b.png','200x170c.png','200x170d.png')
global album_img
#album_img = ('/tmp/kunst.png')
_image = ('/tmp/kunst.jpg')
album_img = ('150x112.png')


#define function that checks for mouse location
def on_click():
	click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
	#check to see if exit has been pressed
	if 396 <= click_pos[0] <= 460 and 14 <= click_pos[1] <=49:
		print "You pressed exit" 
		button(0)


#define action on pressing buttons
def button(number):
	print "You pressed button ",number
	if number == 0:    #specific script when exiting
		screen.fill(black)
		font=pygame.font.Font(None,30)
		subprocess.call("mpc stop", shell=True)
        	label=font.render("      Radioplayer Rocks!!", 1, (white))
        	screen.blit(label,(20,160))
		pygame.display.flip()
		time.sleep(3)
		sys.exit()


def refresh_menu_screen():
       #set up the fixed items on the menu
	#screen.fill(black) #change the colours if needed
        mouse = pygame.mouse.get_pos()

       # pos = pygame.mouse.get_pos()
        current_time = datetime.datetime.now().strftime('%I:%M')
        time_font=pygame.font.Font(None,75)
        time_label = time_font.render(current_time, 1, (cyan))

	font=pygame.font.Font(None,32)
	station_font=pygame.font.Font(None,25)
        skin=pygame.image.load("skin480.png")
	indicator_on=font.render("[        ]", 1, (blue))
        indicator_off=font.render("", 1, (white))
	label2=font.render("Mouse"+str(mouse), 1, (cyan))

	#draw the main elements on the screen ===============================
	album_art=pygame.image.load(album_img)
#	album_art=pygame.transform.scale(album_art, (200, 170))
        screen.blit(skin,(0,0))
        screen.blit(album_art,(17,60))
        #screen.blit(label,(520, 105))
        screen.blit(label2,(190, 62))
	pygame.draw.rect(screen, black, (336, 110, 150, 49),0)
	pygame.draw.rect(screen, black, (52, 186, 407, 74),0)
        screen.blit(time_label,(336, 107))

	##### display the station name and split it into 2 parts : 
	lines = subprocess.check_output("mpc current", shell=True).split("-")
	if len(lines)==1:
		line1 = lines[0]
		line1 = line1[:-1]
		line2 = " No additional info: "
	else:
		line1 = lines[0]
		line2 = lines[1]

	line1 = line1[:38]
	line2 = line2[1:38]
	line2 = line2[:-1]
	#trap no station data
	if line1 =="":
		line2 = "Press PLAY"
		station_status = "Stopped"
		status_font = red
	else:
		station_status = "Playing"
		status_font = green

	station_name=station_font.render(line1, 1, (white))
	additional_data=station_font.render(line2, 1, (white))
	station_label=font.render(station_status, 1, (status_font))
	screen.blit(station_label,(191,117)) #playing
	screen.blit(station_name,(66,350))
	screen.blit(additional_data,(66,231))

	 ##### display remaining time  : 
        RemTime = subprocess.check_output("mpc -f %time%", shell=True).split("\n")
        if len(RemTime)==1:
                Ln1 = RemTime[0]
                Ln1 = Ln1[:-1]
                Ln2 = "> "
        else:
                Ln1 = RemTime[0]
                Ln2 = RemTime[1]

#        Ln1 = Ln1[1:19]
        Ln2 = Ln2[10:]
        rem_time=station_font.render(Ln2, 1, (cyan))
        screen.blit(rem_time,(190,147))

	######## add volume number
	volume = subprocess.check_output("mpc volume", shell=True )
	volume = volume[8:]
	volume = volume[:-1]
	volume_tag=font.render(volume, 1, (white))
	screen.blit(volume_tag,(190,90))
	####### shuffle the list
	if shuffle == 1:
		screen.blit(indicator_on,(513, 102))

	else:
        	screen.blit(indicator_off,(513, 102))
	####### light-up source button
	if mp3 == 1:
		screen.blit(indicator_on,(298, 16))
		screen.blit(indicator_off,(209, 16))
	else:
		screen.blit(indicator_off,(298, 16))
		screen.blit(indicator_on,(209,16))

	pygame.display.flip()


def main():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "screen pressed" #for debugging purposes
                mousex, mousey = pygame.mouse.get_pos()
              #  pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                print (mousex, mousey)
              #  print pos #for checking
                pygame.draw.circle(screen, red, (mousex, mousey), 20, 0) #for debugging purposes - adds a small dot where the screen is pressed
                on_click()

     #ensure there is always a safe way to end the program if the touch screen fails

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
        refresh_menu_screen()

    refresh_menu_screen()
    time.sleep(0.2)


#################### EVERTHING HAS NOW BEEN DEFINED ###########################

#set size of the screen
size = width, height = 480, 320
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
#station_name()
refresh_menu_screen()  #refresh the menu interface 
main() #check for key presses and start emergency exit


