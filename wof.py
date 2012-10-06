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
import os, subprocess
import RPi.GPIO as GPIO

# define song list in array (could make it smart and take the first 12 songs)
def setupSongList(songs):
    song1 = '001.mp3'
    song2 = '002.mp3'
    song3 = '003.mp3'
    song4 = '004.mp3'
    song5 = '005.mp3'
    song6 = '006.mp3'
    song7 = '007.mp3'
    song8 = '008.mp3'
    song9 = '009.mp3'
    song10 = '010.mp3'
    song11 = '011.mp3'
    song12 = '012.mp3'
    songs.append(song1)
    songs.append(song2)
    songs.append(song3)
    songs.append(song4)
    songs.append(song5)
    songs.append(song6)
    songs.append(song7)
    songs.append(song8)
    songs.append(song9)
    songs.append(song10)
    songs.append(song11)
    songs.append(song12)

# define wait time in seconds before playing mp3
waitTime = 6

# setup variables
debounce = []
position = -1
songs = []
sectionChanged = False
print "done initial values"

# play the mp3
def playMP3(songName):
    # so we need to stop, clear, add then play
    stopMP3()
    os.system("sudo mpc add " + songName)
    cmd = subprocess.Popen("sudo mpc play",shell=True, stdout=subprocess.PIPE)
    print "Section : " + songName + " playing.....  " + cmd.stdout.readline()

# stop the mp3
def stopMP3():
    os.system("sudo mpc stop")
    os.system("sudo mpc clear")
    print "stop"

# setup sound and mpd
def setupMPD():
    #os.system("sudo modprobe snd_bcm2835")
    #os.system("sudo amixer cset numid=3 1")
    #os.system("sudo mpd")
    os.system("sudo mpc")
    os.system("sudo mpc clear")
    #os.system("sudo mpc volume 25")
    print "setupMPD"

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
    # 000000001111  bottom  8
    # 000011111100          4
    # 001111000110          2
    # 011001100000  top     1
    # value in binary
    # 013267541118
    #         240
    
    # map the above into array with -1 where invalid
    pos = [0,1,3,2,7,6,4,5,11,-1,10,-1,8,-1,9,-1]
    
    greyValue = 0
    
    # get grey value
    if ( GPIO.input(22) == True ):
        greyValue += 1
    if ( GPIO.input(23) == True ):
        greyValue += 2
    if ( GPIO.input(24) == True ):
        greyValue += 4
    if ( GPIO.input(25)== True ):
        greyValue += 8

    return pos[greyValue]

# to change to BCM GPIO numbering
GPIO.setmode(GPIO.BCM) 

# setup pin directions
GPIO.setup(17, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

#setup pullup resistors on all inputs
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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

playingMusic = False

print "starting loop....."

while True:
    # break loop if button bressed
    if ( GPIO.input(17) == True ):
        break
    # check the inputs
    positionNow = checkInputs()
    
    # update the debounce array
    updateDebounce(debounce, positionNow)
    
    # check the actual position
    # print "get actual position..."
    position = checkPosition(debounce)
    print "position is: " + str(position)
    
    # update allow playing only if the wheel has changed sections from where it stopped last
    # this prevents the same song playing over and over again
    # also stop any currently playing songs
    if position < 0:
        sectionChanged = True
        if playingMusic:
                        stopMP3()
                        playingMusic = False
    
    # play mp3 if position is valid
    if (position >= 0 and sectionChanged):
        sectionChanged = False
        
        # play the required song
        playMP3(songs[position])
        playingMusic = True
        # possibly add control to activate the solenoid to prevent movement
        # would then need to sleep() for the time the mp3 plays
        # then release the solenoid and continue
    
    sleep(0.5);

print "done"
