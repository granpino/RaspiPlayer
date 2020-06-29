#!/usr/bin/python
# RaspiPlayer 480x320
# This is to be used with a 3.5" HDMI touchscreen or equivalent
# Tested with the Raspberry pi 2 and raspbian stretch
# The program must be run within the Lxterminal.
# Current changes include: Selection of folders to be played, or Play everything
# in the USB drive by clicking on Mp3 button.
# Rev2.41 by Granpino

 
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import os
import glob
import random
#import requests # check internet connection
import socket
pygame.init()

#define colors
cyan = 50, 255, 255
blue = 26, 0, 255
black = 0, 0, 0
white = 255, 235, 235
red = 255, 0, 0
green = 0, 255, 0
silver = 192, 192, 192
gray = 40, 40, 40

#other
os.system("mount /dev/sda1 /mnt/usbdrive") #setup for USB drive
subprocess.call("mpc random off", shell=True)
subprocess.call("mpc clear", shell=True)
subprocess.call("mpc volume 65", shell=True)
subprocess.call("mpc update ", shell=True)
subprocess.call("mpc load Radio", shell=True)

clock = pygame.time.Clock()

mp3 = False
shuffle = False
x = 0
PlsPath = "/var/lib/mpd/playlists/"
PlayList = os.listdir( PlsPath )
CurrPlaylist = " "
play = False

#global album_img
_image = ('/tmp/kunst.png')
album_img = ('150x112.png')
connection = None

#set size of the screen
size = width, height = 480, 320
### change screen mode for troubleshooting purposes
#screen = pygame.display.set_mode(size) #,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


#define function that checks for mouse location
def on_click():
	# exit has been pressed
	if 396 < click_pos[0] < 458 and 10 < click_pos[1] < 56:
		print "You pressed exit" 
		button(0)
	# play was pressed
	if 104 <= click_pos[0] <= 192 and 270 <= click_pos[1] <=304:
                print "You pressed  play"
                button(1)

	# folder  was pressed
        if 375 <= click_pos[0] <= 458 and 270 <= click_pos[1] <304:
                print "You pressed folder button"
                button(2)

	# mp3 was pressed
        if 284 <= click_pos[0] <= 371 and 10 <= click_pos[1] <=56:
                print "You pressed  mp3"
                button(3)
	# previous  was pressed
        if 13 <= click_pos[0] <= 103 and 270 <= click_pos[1] <=304:
                print "You pressed  previous"
                button(4)

	 # next  was pressed
        if 195 <= click_pos[0] <= 282 and 270 <= click_pos[1] <=304:
                print "You pressed button next"
                button(5)

	 # volume down was pressed
        if 13 <= click_pos[0] <= 103 and 10 <= click_pos[1] <= 56:
                print "You pressed volume down"
                button(6)

	 # button 7 was pressed
        if 104 <= click_pos[0] <= 192 and 10 <= click_pos[1] <=56:
                print "You pressed volume up"
                button(7)

	 # button 8 was pressed
        if 195 <= click_pos[0] <= 282 and 10 <= click_pos[1] <=56:
                print "You pressed Radio"
                button(8)

	 # button 9 was pressed
        if 284 <= click_pos[0] <= 371 and 270 <= click_pos[1] <=304:
                print "You pressed Shuffle"
                button(9)


#define action on pressing buttons
def button(number):
	global album_img
	global play
	global x
	global CurrPlaylist
	print "You pressed button ",number
	if number == 0:    #time to  exit
		screen.fill(black)
		font=pygame.font.Font(None,30)
		subprocess.call("mpc stop", shell=True)
        	label=font.render("RaspiPlayer Rocks!!", 1, (white))
        	screen.blit(label,(40,150))
		pygame.display.flip()
		time.sleep(2)
		sys.exit()

	if number == 1: # play / stop	
		if play == True:
    	    	    subprocess.call("mpc stop ", shell=True)
		else:
		    subprocess.call("mpc play ", shell=True)  
		play = (1,0)[play]
		album_img = ("/tmp/kunst.png")
		refresh_menu_screen()

	if number == 2: # One playlist for each subdirectory in USB drive.
		try:
                    subprocess.call("mpc clear ", shell=True)
	 	    CurrPlaylist = PlayList[x]
		    CurrPlaylist = CurrPlaylist[:-4]
		    CurrPlaylist = CurrPlaylist[:11]
		except IndexError: # end of playlists.
		    x = 0
                    CurrPlaylist = PlayList[x]
                    CurrPlaylist = CurrPlaylist[:-4]
                    CurrPlaylist = CurrPlaylist[:11]
		print (CurrPlaylist)
	        subprocess.call("mpc load " + str(CurrPlaylist), shell = True)
		subprocess.call("mpc add " + str(CurrPlaylist), shell = True)
        	x = x + 1
		mp3 = True
		play = False
		refresh_menu_screen()

	if number == 8:  # radio
		subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc load Radio ", shell=True)
		global mp3
		mp3 = False
		CurrPlaylist = "Radio"
		refresh_menu_screen() 

	if number == 4:
		subprocess.call("mpc prev ", shell=True)
		refresh_menu_screen()

	if number == 5:
		subprocess.call("mpc next ", shell=True)
		refresh_menu_screen()

	if number == 6:
		subprocess.call("mpc volume -5 ", shell=True)
		refresh_menu_screen()

	if number == 7:
		subprocess.call("mpc volume +5 ", shell=True)
		refresh_menu_screen()

	if number == 9:
                subprocess.call("mpc random ", shell=True)
		global shuffle
		shuffle = (1,0)[shuffle]
		refresh_menu_screen()

        if number == 3: # Single playlist for all files in usb
                subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc add /", shell=True) 
		mp3 = True
		CurrPlaylist = "USB"
                refresh_menu_screen()

def connected():
    """Detect an internet connection."""
    global connection
    connection = None
    try:
        socket.create_connection(("1.1.1.1", 53)) # check every 180 seconds
      #  r.raise_for_status()
        print("Internet connection detected.")
#	return True
        connection = True
    except OSError:
        print("Internet connection not detected.")
        connection = False
    finally:
        return connection


def refresh_menu_screen():
	global connection
        global connect_img
	global CurrPlaylist
        current_time = datetime.datetime.now().strftime('%I:%M')
        time_font=pygame.font.Font(None,70)
        time_label = time_font.render(current_time, 1, (white))

	connect_font=pygame.font.Font(None, 32)
        connect_label = connect_font.render(". .", 1, (white))
        font=pygame.font.Font(None,32)
	station_font=pygame.font.Font(None,28)
        skin1=pygame.image.load("backgnd.png")
        skin2=pygame.image.load("buttons.png")
	indicator_on=font.render("[        ]", 1, (green))
        indicator_off=font.render("", 1, (white))
	label2=font.render("RaspiPlayer", 1, (silver))

        screen.blit(skin1,(0,0))
	screen.blit(skin2,(0,0))
        screen.blit(label2,(190, 62))
	pygame.draw.rect(screen, gray, (336, 95, 130, 49),0)
	pygame.draw.rect(screen, gray, (52, 183, 407, 75),0)
        screen.blit(time_label,(336, 90))
        conn_image=pygame.image.load("internet.png")
        if connection==True:
            screen.blit(conn_image,(418, 62))
        else:
            screen.blit(connect_label,(418, 62))

	try:
	    album_art=pygame.image.load(album_img) # album art
            album_art=pygame.transform.scale(album_art, (155, 117))
	    screen.blit(album_art,(17,60))
	except pygame.error:
	    time.sleep(1)

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
		Playlist_name = (CurrPlaylist)
#		connection = False
	else:
		Playlist_name = (CurrPlaylist)
#		connection = True

	station_name=station_font.render(line1, 1, (white))
	additional_data=station_font.render(line2, 1, (white))
	station_label=font.render(Playlist_name, 1, (cyan))
	screen.blit(station_label,(190,117)) #playing
	screen.blit(station_name,(66,231))
	screen.blit(additional_data,(66,195))

	 ##### display remaining time  : 
        RemTime = subprocess.check_output("mpc -f %time%", shell=True).split("\n")
        if len(RemTime)==1:
                Ln1 = RemTime[0]
                Ln1 = Ln1[:-1]
                Ln2 = "> "
        else:
                Ln1 = RemTime[0]
                Ln2 = RemTime[1]

        Ln2 = Ln2[:-5]
        rem_time=station_font.render(Ln2, 1, (cyan))
        screen.blit(rem_time,(190,153))

	# add volume number
	volume = subprocess.check_output("mpc volume", shell=True )
	volume = volume[8:] # remove unwanted characters.
	volume = volume[:-1]
	volume_tag=font.render(volume, 1, (white))
	screen.blit(volume_tag,(190,90))
	# shuffle the list
	if shuffle == 1:
		screen.blit(indicator_on,(300, 273))

	else:
        	screen.blit(indicator_off,(373, 273))
	# light-up source button
	if mp3 == True:
		screen.blit(indicator_on,(298, 16))
		screen.blit(indicator_off,(209, 16))
	else:
		screen.blit(indicator_off,(298, 16))
		screen.blit(indicator_on,(209,16))
#	time.sleep(.3)
	pygame.display.flip()

def main():
    global click_pos
    timer = pygame.time.get_ticks()
    while 1:
        seconds=(pygame.time.get_ticks() - timer)/1000
        if seconds > 180: # check every 3 min 
	    timer = pygame.time.get_ticks()
            connected() # check for internet connection

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                print "screen pressed" #for debugging purposes
                print click_pos #for checking coordinates
                on_click()

            #Press ESC key on the computer to end while in VNC

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # ESC key will kill it
                    sys.exit()
        clock.tick(15) #refresh screen 15fps 
        refresh_menu_screen()

connected()
refresh_menu_screen() 
main() # Main loop


