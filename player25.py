#!/usr/bin/python
# -*- coding: utf-8 -*-
# RaspiPlayer 640x430 - LARGE -screen
# This is to be used with a 3.5" HDMI touchscreen or equivalent
# Tested with the Raspberry pi 2 and raspbian stretch
# The program must be run within the Lxterminal.
# 
# 
# Rev2.5 by Granpino
 
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import os
import random
import socket

pygame.init()
pygame.font.init()

cyan = 50, 255, 255
blue = 0, 0, 255
black = 0, 0, 0
white = 255, 235, 235
red = 255, 0, 0
green = 0, 255, 0
silver = 192, 192, 192
gray = 40, 40, 40

#other
os.system("mount /dev/sda1 /mnt/usbdrive") #setup for USB drive
subprocess.call("mpc stop", shell=True)
subprocess.call("mpc random off", shell=True)
subprocess.call("mpc clear", shell=True)
subprocess.call("mpc update ", shell=True)
subprocess.call("mpc load Radio", shell=True)
volume = subprocess.check_output("mpc volume", shell=True )
volume = volume[-4:-1] # remove unwanted characters.

clock = pygame.time.Clock()

# make sure to change the settings at /boot/config.txt for the
# resolution required. Do this after installing the screen driver.
q = 1.33 # screen size ratio. Use 1 for 480x320,or 1.333 for 640x430.

mp3 = False
shuffle = False
x = 0
PlsPath = "/var/lib/mpd/playlists/"
PlayList = os.listdir( PlsPath )
CurrPlaylist = "Radio "
play = False
str1 = 0

_image = ('/tmp/kunst.png')
album_img = ('150x112.png')
conn_image=pygame.image.load("internet.png")
genlist_img=pygame.image.load("genlist2.png")
skin1=pygame.image.load("640x430.png")
skin2=pygame.image.load("buttons.png")

connection = None

#set size of the screen
size = width, height = 640, 430
### change screen mode for troubleshooting purposes
#screen = pygame.display.set_mode(size) #,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

#define function that checks for mouse location
def on_click():
	# exit has been pressed
	if int(396*q) < click_pos[0] < round(458*q, 0) and round(10*q, 0) < click_pos[1] < round(56*q, 0):
		button(0)
	# play - was pressed
	if round(104*q, 0) <= click_pos[0] <= round(192*q, 0) and round(270*q, 0) <= click_pos[1] <=round(304*q, 0):
		button(1)

	# folder -  was pressed
	if round(375*q,0) <= click_pos[0] <= round(458*q,0) and round(270*q,0) <= click_pos[1] <round(304*q,0):
		button(2)

	# mp3 - was pressed
	if round(284*q,0) <= click_pos[0] <= round(371*q,0) and round(10*q,0) <= click_pos[1] <=round(56*q,0):
		button(3)
	# previous -  was pressed
	if round(13*q,0) <= click_pos[0] <= round(103*q,0) and round(270*q,0) <= click_pos[1] <=round(304*q,0):
		button(4)

	 # next -  was pressed
	if round(195*q,0) <= click_pos[0] <= round(282*q,0) and round(270*q,0) <= click_pos[1] <=round(304*q,0):
		button(5)

	 # volume down -6  was pressed
	if int(13*q) <= click_pos[0] <= int(103*q) and int(10*q) <= click_pos[1] <= int(56*q):
		button(6)

	 # volume up  7 was pressed
	if round(104*q,0) <= click_pos[0] <= round(192*q,0) and round(10*q,0) <= click_pos[1] <=round(56*q,0):
		button(7)

	 # Radio - 8 was pressed
	if round(195*q,0) <= click_pos[0] <= round(282*q,0) and round(10*q,0) <= click_pos[1] <=round(56*q,0):
		button(8)

	 # button 9 was pressed
	if round(284*q,0) <= click_pos[0] <= round(371*q,0) and round(270*q,0) <= click_pos[1] <=round(304*q,0):
		button(9)

	 # USB scan - 10, button  was pressed
	if round(410*q,0) <= click_pos[0] <= round(458*q,0) and round(62*q,0) <= click_pos[1] <=round(100*q,0):
		button(10)

     # seek - 11, button was pressed
	if round(52*q,0) <= click_pos[0] <= round(458*q,0) and round(250*q,0) <= click_pos[1] <=round(275*q,0):
		button(11)

#define action on pressing buttons
def button(number):
	global album_img
	global play
	global x
	global CurrPlaylist
	global seek
	global mp3
	global volume
	if number == 0:    #time to  exit
		font = pygame.font.SysFont('sans', 20, bold=0)
		btn_label1 = font.render("Exit", 1, (white))
		btn_label2 = font.render("Shutdown", 1, (white))
		while 1:
			pygame.draw.rect(screen, white, (int(52*q), int(183*q), int(407*q), int(85*q)),0)
			pygame.draw.rect(screen, gray, (int(270*q), int(230*q), int(83*q), int(30*q)),0)
			pygame.draw.rect(screen, gray, (int(370*q), int(230*q), int(83*q), int(30*q)),0)
			screen.blit(btn_label1,(int(300*q),int(235*q)))
			screen.blit(btn_label2,(int(380*q),int(235*q)))
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					click_pos = pygame.mouse.get_pos()
					if round(270*q,0) < click_pos[0] < round(350*q,0) and round(230*q,0) < click_pos[1] < round(260*q,0):
						subprocess.call("mpc stop", shell=True)
						sys.exit()
					if round(370*q,0) < click_pos[0] < round(450*q,0) and round(230*q,0) < click_pos[1] < round(260*q,0):
	#					screen.blit(Label1,(int(66*q),int(231*q)))
						pygame.display.flip()
						subprocess.call("mpc stop", shell=True)
						os.system("sudo shutdown -h now")
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE: # ESC to exit
						subprocess.call("mpc stop", shell=True)
						sys.exit()
			pygame.display.flip()
		time.sleep(1)
		pygame.display.flip()

	if number == 1: # play / pause
		if play == True:
			subprocess.call("mpc pause ", shell=True)
		else:
			subprocess.call("mpc play ", shell=True)
		play = (1,0)[play] # toggle play 
		album_img = ("/tmp/kunst.png")
	#	refresh_screen()

	if number == 2: # FOLDER PLAY.
		usbdrv2 = subprocess.check_output("ls /mnt/usbdrive", shell=True)
		if len(usbdrv2)==0: # is USB connected?
			CurrPlaylist = "No USB!"
			return
		else:
			try:
				subprocess.call("mpc clear", shell=True)
				CurrPlaylist = PlayList[x]
				CurrPlaylist = CurrPlaylist[:-4] #remove .m3u
				CurrPlaylist = CurrPlaylist[:13]
			except IndexError: # end of playlists.
				x = 0
				CurrPlaylist = PlayList[x]
				CurrPlaylist = CurrPlaylist[:-4] #remove .m3u
				CurrPlaylist = CurrPlaylist[:13]
			subprocess.call("mpc load " + str(CurrPlaylist), shell = True)
			subprocess.call("mpc add " + str(CurrPlaylist), shell = True)
			x = x + 1
			if CurrPlaylist == "Radio":
				mp3 = False
				play = False
			else:
				mp3 = True
				play = False
			#	refresh_screen()

	if number == 3: # MP3 PLAY
		usbdrv = subprocess.check_output("ls /mnt/usbdrive", shell=True)
		if len(usbdrv)==0:  # is USB connected?
			CurrPlaylist = "No USB!"
			return
		else:
			subprocess.call("mpc clear ", shell=True)
			subprocess.call("mpc add /", shell=True) 
			mp3 = True
			play = False
			CurrPlaylist = "USB"
			#refresh_screen()

	if number == 4:
		if play == True:
			subprocess.call("mpc prev ", shell=True)
	#	refresh_screen()

	if number == 5:
		if play == True:
			subprocess.call("mpc next ", shell=True)
			#play = True
	#	refresh_screen()

	if number == 6:
		subprocess.call("mpc volume -5 ", shell=True)
		volume = subprocess.check_output("mpc volume", shell=True)
		volume = volume[-4:-1] # remove unwanted characters.
	#	refresh_screen()

	if number == 7:
		subprocess.call("mpc volume +5 ", shell=True)
		volume = subprocess.check_output("mpc volume", shell=True)
		volume = volume[-4:-1] # remove unwanted characters.
	#	refresh_screen()

	if number == 8:  # Radio
		subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc load Radio ", shell=True)
		#global mp3
		mp3 = False
		CurrPlaylist = "Radio"
		play = False
	#	refresh_screen() 

	if number == 9:
		subprocess.call("mpc random ", shell=True)
		global shuffle
		shuffle = (1,0)[shuffle]
	#	refresh_screen()

	if number == 10: # Scan USB
		font = pygame.font.SysFont('sans', 20, bold=0)
		Label1=font.render("Scanning USB for Mp3 files...", 1, (black))
		Label2=font.render("Generate USB playlists.", 1, (black))
		btn_label1 = font.render(" Cancel", 1, (black))
		btn_label2 = font.render("OK", 1, (black))
		while 1:
			pygame.draw.rect(screen, white, (int(52*q), int(183*q), int(407*q), int(85*q)),0)
			pygame.draw.rect(screen, cyan, (int(270*q), int(230*q), int(83*q), int(30*q)),0)
			pygame.draw.rect(screen, cyan, (int(370*q), int(230*q), int(83*q), int(30*q)),0)
			screen.blit(Label2,(int(66*q),int(195*q)))
			screen.blit(btn_label1,(int(278*q),int(235*q)))
			screen.blit(btn_label2,(int(400*q),int(235*q)))
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					click_pos = pygame.mouse.get_pos()
					if round(270*q,0) < click_pos[0] < round(350*q,0) and round(230*q,0) < click_pos[1] < round(260*q,0):
						return
					if round(370*q,0) < click_pos[0] < round(450*q,0) and round(230*q,0) < click_pos[1] < round(260*q,0):
						screen.blit(Label1,(int(66*q),int(231*q)))
						pygame.display.flip()
						subprocess.call("./generate-playlist.sh", shell=True)
						subprocess.call("mpc clear", shell=True)
						subprocess.call("mpc update", shell=True)
						return
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE: # ESC to exit
						sys.exit()

			pygame.display.flip()
		time.sleep(1)
		pygame.display.flip()

	if number == 11:
		if mp3 == True:
			atseek = (seek-70)*100 / 540 #Formula: (x-inMin)(outMax-outMin) / (inMax-inMin)+outMin
			subprocess.call("mpc seek " + str(atseek) + "%", shell=True)
		else:
			return

def connected():
    #Detect an internet connection
    global connection
    connection = None
    try:
        socket.create_connection(("1.1.1.1", 53)) # check every 180 seconds
#        print("Internet connection detected.")
        connection = True
    except OSError:
#        print("Internet connection not detected.")
        connection = False
    finally:
        return connection

def show_current():
 ##### display the station name and split it into 2 parts : 
    try:
        tag = subprocess.check_output("mpc current", shell=True).split(" - ")
    except subprocess.CalledProcessError:
      #  subprocess.call("mpc next", shell=True)
        return
    if len(tag)==1:
        artist = tag[0]
        title = " RaspiPlayer: "
    else:
        artist = tag[0]
        title = tag[1]

    artist = artist[:38]
    title = title[:38]
    title = title[:-1]
    #trap no station data
    if artist =="":
        title = "Press PLAY"
        Playlist_name = (CurrPlaylist)
        play = False
    else:
        Playlist_name = (CurrPlaylist)

    artist_name=sfont.render(artist, 1, (white))
    title_lbl=sfont.render(title, 1, (white))
    playlist_label=sfont.render(Playlist_name, 1, (cyan))
    screen.blit(playlist_label,(int(190*q),int(120*q))) #playlist
    screen.blit(artist_name,(int(66*q),int(225*q)))
    screen.blit(title_lbl,(int(66*q),int(195*q)))

def Rem_time():
    pygame.draw.line(screen, black, (52*q, 260*q), (459*q, 260*q), 10)

     ## display remaining time
    try: 
	    RemTime = subprocess.check_output("mpc -f  %time%", shell=True).split("\n")
    except subprocess.CalledProcessError:
        return
    if len(RemTime)==0:
        remT1 = RemTime[0]
        remT1 = remT1[:-1]

    else:
        remT1 = RemTime[0]
        remT2 = RemTime[1]

    if mp3 == True and play == True:  #Draw bargraph
        try:
            str1 = remT2[-5:-2]
            str1 = str1.replace("(", '')
            str1 = int(str1)
            pygame.draw.line(screen, green, (52*q, 260*q), (52*q + (str1*5.4), 260*q), 8)
        except ValueError:
            subprocess.call("mpc stop", shell=True)
            print('value error')
    remT2 = remT2[:-5]
    rem_time=sfont.render(remT2, 1, (cyan))
    screen.blit(rem_time,(int(190*q),int(153*q)))

def refresh_screen():
	global connect_img
	global CurrPlaylist
	global play
	global sfont
	global str1
	global volume
	lfont=pygame.font.Font(None, int(70*q))
	mfont=pygame.font.Font(None, int(32*q))
	sfont=pygame.font.Font(None, int(28*q))

	current_time = datetime.datetime.now().strftime('%I:%M')
	time_label = lfont.render(current_time, 1, (white))
	connect_label = mfont.render(". .", 1, (green))
	Raspi_lbl=mfont.render("RaspiPlayer", 1, (white))

	screen.blit(skin1,(0,0))
	screen.blit(Raspi_lbl,(int(190*q), int(62*q)))

	pygame.draw.rect(screen, gray, (int(336*q), int(95*q), int(130*q), int(49*q)),0)
	pygame.draw.rect(screen, gray, (int(52*q), int(183*q), int(407*q), int(75*q)),0)
	screen.blit(genlist_img,(int(427*q), int(57*q)))
	screen.blit(time_label,(int(340*q), int(93*q)))

	if connection==True:
		screen.blit(conn_image,(int(397*q), int(62*q)))
	else:
		screen.blit(connect_label,(int(397*q), int(62*q)))

	try:
		album_art=pygame.image.load(album_img) # album art
		album_art=pygame.transform.scale(album_art, (int(155*q), int(117*q)))
		screen.blit(album_art,(int(17*q),int(60*q)))
	except pygame.error:
		time.sleep(1)

	##### display the station name and split it into 2 parts : 
	show_current()
        #remaining time
	Rem_time()
	# add volume number
#	volume = subprocess.check_output("mpc volume", shell=True )
#	volume = volume[-4:-1] # remove unwanted characters.
	volume_lbl=mfont.render(volume, 1, (white))
	screen.blit(volume_lbl,(int(190*q),int(90*q)))
	# change color of buttons.
	if shuffle == True:
		pygame.draw.rect(screen, green, (int(300*q), int(280*q), int(70*q), int(20*q)),0)
	else:
		pygame.draw.rect(screen, white, (int(300*q), int(280*q), int(70*q), int(20*q)),0)
	if mp3 == True:
		pygame.draw.rect(screen, green, (int(290*q), int(20*q), int(70*q), int(20*q)),0)
		pygame.draw.rect(screen, white, (int(200*q), int(20*q), int(70*q), int(20*q)),0)
	else:
		pygame.draw.rect(screen, white, (int(290*q), int(20*q), int(70*q), int(20*q)),0)
		pygame.draw.rect(screen, green, (int(200*q), int(20*q), int(70*q), int(20*q)),0)

	if play == True:
		pygame.draw.rect(screen, green, (int(110*q), int(280*q), int(70*q), int(20*q)),0)
	else:
		pygame.draw.rect(screen, white, (int(110*q), int(280*q), int(70*q), int(20*q)),0)

	screen.blit(skin2,(0,0))
	pygame.display.flip()

def main():
	global click_pos
	global seek
	timer = pygame.time.get_ticks()
	while 1:
		seconds=(pygame.time.get_ticks() - timer)/1000
		if seconds > 180: # check every 3 min 
			timer = pygame.time.get_ticks()
			connected() # check for internet connection

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				click_pos = event.pos
			#	print (event)
			#	print (event.pos)
				seek = event.pos[0] # click position x
				on_click()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE: # ESC key will kill it
					sys.exit()
		clock.tick(10) #refresh screen 8fps 
		refresh_screen()
	pygame.quit()

connected()
refresh_screen() 
main() 


