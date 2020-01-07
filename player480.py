#!/usr/bin/python
# RaspiPlayer 480x320
# This is to be used with a 3.5" HDMI touchscreen or equivalent
# Tested with the Raspberry pi 2 and raspbian stretch
# The program must be run within the Lxterminal
# Rev2.3 
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import os
import glob
import random
import requests # check internet connection

pygame.init()

#define colors
cyan = 50, 255, 255
blue = 26, 0, 255
black = 0, 0, 0
white = 255, 235, 235
red = 255, 0, 0
green = 0, 255, 0
silver = 192, 192, 192

#other
os.system("mount /dev/sda1 /mnt/usbdrive") #setup for USB drive
subprocess.call("mpc random off", shell=True)
subprocess.call("mpc clear", shell=True)
subprocess.call("mpc volume 65", shell=True)
subprocess.call("mpc update ", shell=True)
subprocess.call("mpc load playlist", shell=True)


mp3 = False
shuffle = False

#global album_img
_image = ('/tmp/kunst.png')
album_img = ('150x112.png')
connection = None


#define function that checks for mouse location
def on_click():
#	click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
	#check to see if exit has been pressed
	if 396 < click_pos[0] < 460 and 10 < click_pos[1] < 56:
		print "You pressed exit" 
		button(0)
	#now check to see if play was pressed
	if 131 <= click_pos[0] <= 237 and 270 <= click_pos[1] <=304:
                print "You pressed button play"
                button(1)
	#now check to see if stop  was pressed
#        if 320 <= click_pos[0] <= 473 and 410 <= click_pos[1] <460:
#                print "You pressed button stop"
#                button(2)
	#now check to see if mp3 was pressed
        if 284 <= click_pos[0] <= 371 and 10 <= click_pos[1] <=56:
                print "You pressed button mp3"
                button(3)
	#now check to see if previous  was pressed
        if 22 <= click_pos[0] <= 128 and 270 <= click_pos[1] <=304:
                print "You pressed button previous"
                button(4)

	 #now check to see if next  was pressed
        if 241 <= click_pos[0] <= 348 and 270 <= click_pos[1] <=304:
                print "You pressed button next"
                button(5)

	 #now check to see if volume down was pressed
        if 13 <= click_pos[0] <= 103 and 10 <= click_pos[1] <= 56:
                print "You pressed volume down"
                button(6)

	 #now check to see if button 7 was pressed
        if 104 <= click_pos[0] <= 192 and 10 <= click_pos[1] <=56:
                print "You pressed volume up"
                button(7)

	 #now check to see if button 8 was pressed
        if 195 <= click_pos[0] <= 282 and 10 <= click_pos[1] <=56:
                print "You pressed radio"
                button(8)

	 #now check to see if button 9 was pressed
        if 351 <= click_pos[0] <= 457 and 270 <= click_pos[1] <=304:
                print "You pressed shuffle"
                button(9)


#define action on pressing buttons
def button(number):
	global album_img
	print "You pressed button ",number
	if number == 0:    #specific script when exiting
		screen.fill(black)
		font=pygame.font.Font(None,30)
		subprocess.call("mpc stop", shell=True)
        	label=font.render("RaspiPlayer Rocks!!", 1, (white))
        	screen.blit(label,(40,150))
		pygame.display.flip()
		time.sleep(2)
		sys.exit()

	if number == 1: # play / pause	
		subprocess.call("mpc toggle ", shell=True)
		album_img = ("/tmp/kunst.png")
		refresh_menu_screen()

	if number == 2:
		subprocess.call("mpc stop ", shell=True)
		refresh_menu_screen()

	if number == 8:  # radio
		subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc load playlist ", shell=True)
		global mp3
		mp3 = False
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

        if number == 3: # play Mp3
                subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc update ", shell=True)
		subprocess.call("mpc add /", shell=True) 
		mp3 = True
                refresh_menu_screen()

def internet():
    """Detect an internet connection."""
    global connection
    connection = None
    try:
        r = requests.get("https://google.com")
        r.raise_for_status()
        print("Internet connection detected.")
        connection = True
    except:
        print("Internet connection not detected.")
        connection = False
    finally:
        return connection


def refresh_menu_screen():
        global connect_img
#set up the fixed items on the menu
	#cpu = os.popen("vcgencmd measure_temp").readline()
	#cpu = cpu[-7:] #remove characters not needed
	#cpu = cpu[:-1]
        current_time = datetime.datetime.now().strftime('%I:%M')
        time_font=pygame.font.Font(None,70)
        time_label = time_font.render(current_time, 1, (white))
	#cpu_font=pygame.font.Font(None,32) 
	#cpu_label = cpu_font.render(cpu, 1, (silver)) 
#        global connection
	connect_font=pygame.font.Font(None, 32)
        connect_label = connect_font.render(". .", 1, (white))
        font=pygame.font.Font(None,32)
	station_font=pygame.font.Font(None,28)
        skin=pygame.image.load("skin480.png")
	indicator_on=font.render("[        ]", 1, (blue))
        indicator_off=font.render("", 1, (white))
	label2=font.render("RaspiPlayer", 1, (silver))

	#draw the main elements on the screen 
        screen.blit(skin,(0,0))
        #screen.blit(cpu_label,(398, 62)) #cputemp
 #       screen.blit(connect_label,(398, 62)) 
        screen.blit(label2,(190, 62))
	pygame.draw.rect(screen, black, (336, 95, 130, 49),0)
	pygame.draw.rect(screen, black, (52, 188, 407, 71),0)
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
	    #refresh_menu_screen()
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
		status_font = cyan
	else:
		station_status = " "
		status_font = cyan

	station_name=station_font.render(line1, 1, (white))
	additional_data=station_font.render(line2, 1, (white))
	station_label=font.render(station_status, 1, (status_font))
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

#        Ln1 = Ln1[1:19]
        Ln2 = Ln2[:-5]
        rem_time=station_font.render(Ln2, 1, (cyan))
        screen.blit(rem_time,(190,153))

	######## add volume number
	volume = subprocess.check_output("mpc volume", shell=True )
	volume = volume[8:]
	volume = volume[:-1]
	volume_tag=font.render(volume, 1, (white))
	screen.blit(volume_tag,(190,90))
	####### shuffle the list
	if shuffle == 1:
		screen.blit(indicator_on,(373, 273))

	else:
        	screen.blit(indicator_off,(373, 273))
	####### light-up source button
	if mp3 == True:
		screen.blit(indicator_on,(298, 16))
		screen.blit(indicator_off,(209, 16))
	else:
		screen.blit(indicator_off,(298, 16))
		screen.blit(indicator_on,(209,16))
	time.sleep(.3)
	pygame.display.flip()


def main():
    global click_pos
    while 1:
        internet()
        print(connection)
        for x in range(40): # loop for a while then check internet.
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    print "screen pressed" #for debugging purposes
                    print click_pos #for checking
                    on_click()

            #ensure there is always a safe way to end the 

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: # ESC key will kill it
                        sys.exit()
            refresh_menu_screen()
    time.sleep(0.2)

#################### EVERTHING HAS NOW BEEN DEFINED ###########################
#set size of the screen
size = width, height = 480, 320
#screen = pygame.display.set_mode(size) #,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
refresh_menu_screen()  #refresh the menu interface 
main() #check for key presses and start emergency exit


