wof
=====

## Created for an exhibition piece

wof reads an encoder mounted on the bottom of the wheel with 4 optical sensors and determines the position of the wheel. After the wheel has been turned and stops the associated mp3 for that section is played out the raspberry pi 3.5mm audio plug.

uses 4 couplers setup with greycode to define 12 sections of a wheel.
circuit as below (Resistors need to be confirmed)


![schematic](https://github.com/threldor/wof/raw/master/forkCouplerSchematic.jpg)

after defined time the given mp3 is played for that section

an example encoder wheel is given below

![preview thumb](https://github.com/threldor/wof/raw/master/encoder.png)

## Install Instructions

you will need a working raspberry pi
I used the guide from adafruit [here](http://learn.adafruit.com/adafruit-raspberry-pi-educational-linux-distro) and put on occidentalis

You also need to setup
* [audio output to 3.5mm and mpg321](http://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-audio)
* [python](http://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio)
* [RPi.GPIO](http://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio)
* your wiring as per the scematic