#!/usr/bin/env python

# code written by James Connor
# uses 4 couplers setup with greycode to define 12 sections of a wheel.
# circuit as below (Resistors need to be confirmed)

#                GPIO 
#                 | 
#                R 1k      coupler
#                 |     .............
# 3.3V----R 10k---|-----:---C B E---:----GND
#                       :     ^     :
#                       :     ^     :
#                       :     ^     :
# 5V------R 220---------:---diode---:----GND
#                       :           :
#                       .............
#
# after defined time the given mp3 is played for that section

from time import sleep
import os
import RPi.GPIO as GPIO

# define song list in array (could make it smart and take the first 12 songs)
def setupSongList(songs):
	song1 = '001-FeelSoGood.mp3'
	song2 = '002-LoveFoolosophy.mp3'
	song3 = '003-ReadyForTheFloor.mp3'
	song4 = '004-AndIWasABoyFromSchool.mp3'
	song5 = '005-DANCE.mp3'
	song6 = '006-Newjack.mp3'
	songs.append(song1)
	songs.append(song2)
	songs.append(song3)
	songs.append(song4)
	songs.append(song5)
	songs.append(song6)

# define wait time in seconds before playing mp3
waitTime = 3

# setup variables
debounce = []
position = -1
songs[]
sectionChanged = False
coupler1 = 17
coupler2 = 23
coupler3 = 24
coupler4 = 25

# play the mp3
def playMP3(songName):
	# so we need to stop, clear, add then play
	stopMP3()
	os.system("C:\\Portable\\mpc\\mpc.exe add " + songName)
	cmd = subprocess.Popen("C:\\Portable\\mpc\\mpc.exe play",shell=True, stdout=subprocess.PIPE)
	print "Section : " + str(section) + " playing.....  " + cmd.stdout.readline()

# stop the mp3
def stopMP3():
	os.system("C:\\Portable\\mpc\\mpc.exe stop")
	os.system("C:\\Portable\\mpc\\mpc.exe clear")

# setup sound and mpd
def setupMPD():
	os.system("sudo modprobe snd_bcm2835")
	os.system("sudo amixer cset numid=3 1")
	os.system("sudo mpd")
	os.system("sudo mpc")
	os.system("sudo mpc clear")
	os.system("sudo mpc volume 25")

# create the debounce array with length waitTime
def setupDebounce(waitTime, debounce):
	var = waitTime
	while var > 0:
		debounce.append(-1)
		var -= 1

# update the debounce array with new position
def updateDebounce(debounce, position):
    for index in range(len(debounce)):
        if index == (len(debounce) - 1):
            debounce[index] = position
        else:
            debounce[index] = debounce[index+1]

# check the debounce array and return position or -1 if unknown
def checkPosition(debounce):
    pos = debounce[0]
    for deb in debounce:
        if pos != deb:
            return -1
    return pos
	
# check inputs 
# returns -1 if invalid otherwise returns number from 0 to 11
def checkInputs():
	# greycode goes
	# 0123456789AB  segment number where A is 10 and B is 11
	# 000000001111  inside  8
	# 000011111100          4
	# 001111000110          2
	# 011001100000  oustide 1
	# value in binary
	# 013267541118
	#         240
	
	# map the above into array with -1 where invalid
	pos = [0,1,3,2,7,6,4,5,11,-1,10,-1,8,-1,9,-1]
	
	greyValue = 0
	
	# get grey value
	if ( GPIO.input(coupler1) == False ):
		greyValue += 1
	if ( GPIO.input(coupler2) == False ):
		greyValue += 2
	if ( GPIO.input(coupler3) == False ):
		greyValue += 4
	if ( GPIO.input(coupler4)== False ):
		greyValue += 8
	
	return pos[greyValue]

# to change to BCM GPIO numbering
GPIO.setmode(GPIO.BCM) 

# setup pin directions
GPIO.setup(coupler1, GPIO.IN)
GPIO.setup(coupler2, GPIO.IN)
GPIO.setup(coupler3, GPIO.IN)
GPIO.setup(coupler4, GPIO.IN)

#setup pullup resistors on all inputs
#GPIO.setup(coupler1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(coupler2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(coupler3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(coupler4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
# setup song list
setupSongList(songs)
# setup debounce array
setupDebounce(waitTime, debounce)
# setup sound and MPD
setupMPD()

while True:
	# check the inputs
	positionNow = checkInputs()
	
	# update the debounce array
	updateDebounce(debounce, positionNow)
	
	# check the actual position
	position = checkPosition(debounce)
	
	# update allow playing only if the wheel has changed sections from where it stopped last
	# this prevents the same song playing over and over again
	# also stop any currently playing songs
	if position < 0:
		sectionChanged = True
		stopMP3()
	
	# play mp3 if position is valid
	if (position >= 0 and sectionChanged):
		sectionChanged = False
		
		# play the required song
		playMP3(songs[position])
		# possibly add control to activate the solenoid to prevent movement
		# would then need to sleep() for the time the mp3 plays
		# then release the solenoid and continue
	
	sleep(1);

print "done"