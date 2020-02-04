#!/usr/bin/python
# This script will generate coordinates of the buttons
# to be used when making a new skin.
# This is to be used with a 3.5" HDMI touchscreen
# Tested with the Raspberry pi 2 and raspbian stretch
# The program must be run within the Lxterminal.
#  By; Granpino
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
		font=pygame.font.Font(None,30)
		screen.fill(black)
        	label=font.render("      Radioplayer Rocks!!", 1, (white))
        	screen.blit(label,(20,160))
		pygame.display.flip()
		time.sleep(3)
		sys.exit()


def refresh_menu_screen(): # Draw everything
        mouse = pygame.mouse.get_pos()
        current_time = datetime.datetime.now().strftime('%I:%M')
        time_font=pygame.font.Font(None,75)
        time_label = time_font.render(current_time, 1, (cyan))

	font=pygame.font.Font(None,32)
	station_font=pygame.font.Font(None,25)
        skin=pygame.image.load("skin480e.png") # this is the name of the skin

	label2=font.render("Mouse"+str(mouse), 1, (cyan))

	album_art=pygame.image.load(album_img)
        screen.blit(skin,(0,0))
        screen.blit(album_art,(17,60))
        screen.blit(label2,(190, 62))
	pygame.draw.rect(screen, black, (336, 110, 150, 49),0)
	pygame.draw.rect(screen, black, (52, 186, 407, 74),0)
        screen.blit(time_label,(336, 107))

	song_title=station_font.render("Song Title", 1, (red))
	artist_data=station_font.render("Artist data", 1, (white))
	source_label=font.render("Source Label", 1, (red))
	screen.blit(source_label,(191,117))
	screen.blit(artist_data,(66,231))
        rem_time=station_font.render("Time keeping line", 1, (cyan))
        screen.blit(rem_time,(190,147))
	screen.blit(song_title, (66, 195))
	volume_tag=font.render("65%", 1, (white))
	screen.blit(volume_tag,(190,90))
	pygame.display.flip()


def main():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "screen pressed" #for debugging purposes
                mousex, mousey = pygame.mouse.get_pos()
                print (mousex, mousey)
              #  print pos #for checking
                pygame.draw.circle(screen, red, (mousex, mousey), 20, 0) #for debugging purposes - adds a small dot where the screen is pressed
                on_click()

     # safe way to end 

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
        refresh_menu_screen()

    refresh_menu_screen()
    time.sleep(0.2)


size = width, height = 480, 320
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
refresh_menu_screen() 
main() 


