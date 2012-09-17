wof
=====

**Created for an exhibition piece**

wof reads an encoder mounted on the bottom of the wheel with 4 optical sensors and determines the position of the wheel. After the wheel has been turned and stops the associated mp3 for that section is played out the raspberry pi 3.5mm audio plug.

uses 4 couplers setup with greycode to define 12 sections of a wheel.
circuit as below (Resistors need to be confirmed)

                         coupler
                      .............
3.3V----R 10k---|-----:---C B E---:----GND
                |     :     ^     :
              GPIO    :     ^     :
                      :     ^     :
5V------R 330---------:---diode---:----GND
                      :           :
                      .............

after defined time the given mp3 is played for that section

an example encoder wheel is given below

![preview thumb](https://github.com/threldor/wof/raw/master/encoder.png)