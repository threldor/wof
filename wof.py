#!/usr/bin/env python

# code written by James Connor
# uses 4 couplers setup with greycode to define 12 sections of a wheel.
# circuit as below (Resistors need to be confirmed)
#                          coupler
#                       .............
# 3.3V----R 10k---|-----:---C B E---:----GND
#                 |     :     ^     :
#               GPIO    :     ^     :
#                       :     ^     :
# 5V------R 330---------:---diode---:----GND
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
	songs.append(song1)
	songs.append(song2)
	songs.append(song3)

# define wait time in seconds before playing mp3
waitTime = 3

# setup variables
debounce = []
position = -1
songs[]
allowPlaying = False

# play the mp3
def playMP3(songName):
	os.system('mpg321 ' + songName + ' &')

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
	if ( GPIO.input(22) == False ):
		greyValue += 1
	if ( GPIO.input(23) == False ):
		greyValue += 2
	if ( GPIO.input(24) == False ):
		greyValue += 4
	if ( GPIO.input(25)== False ):
		greyValue += 8
	
	return pos[greyValue]

# to change to BCM GPIO numbering
GPIO.setmode(GPIO.BCM) 

# setup pin directions
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

#setup pullup resistors on all inputs
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
# setup song list
setupSongList(songs)
# setup debounce array
setupDebounce(waitTime, debounce)

while True:
	# check the inputs
	position = checkInputs()
	
	# update the debounce array
	updateDebounce(debounce, position)
	
	# check position
	position = checkPosition(debounce)
	
	# update allow playing only if the wheel has moved from where it stopped last
	# this prevents the same cong playing over and over again
	if position < 0:
		allowPlaying = True
	
	# play mp3 if position is valid
	if (position >= 0 and allowPlaying):
		allowPlaying = False
		
		# play the required song
		playMP3(songs[position])
		# possibly add control to activate the solenoid to prevent movement
		# would then need to sleep() for the time the mp3 plays
		# then release the solenoid and continue
	
	sleep(1);