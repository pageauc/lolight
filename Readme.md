# lolight.py
#### python3 picamera2 Create Low Light Timelapse Images Demo

## Introduction
Written as a test/learning program to help convert pi-timolo https://github.com/pageauc/pi-timolo
to use the picamera2 python3 module.
Different methods were tried for automating settings for low light/day light timelapse images.
This program was useful for trying and testing differnt ideas.
I cleaned it up a bit and posted on GitHub to share with others who may find it useful.

## Install or Upgrade
***IMPORTANT*** - Update Raspberry Pi Operating System To ensure your system is up-to-date.
In SSH or Terminal Session run commands below.

    sudo apt update
    sudo apt upgrade -y

#### Step 1
Select copy icon on right of Github command box below  
or Alternatively with mouse left button highlight curl command in code box below. Right click mouse in **highlighted** area and Copy.     

    curl -L https://raw.github.com/pageauc/lolight/master/install.sh | bash

#### Step 2
On RPI putty SSH or Terminal session, right click, select paste then Enter to download and run install.sh script.

***NOTE*** If config.py exists it will Not be overwritten. A config.py.new will be created/updated instead.
To update existing config.py perform commands below

    cd ~/lolight
    cp config.py config.py.bak
    cp config.py.new config.py

## Edit Settings
To review and/or change settings execute command below in SSH or terminal session.
See comments for each variable setting. Ensure camera is installed and working.

    cd ~/lolight
    nano config.py

To exit nano and save changes press

    ctrl-x y

## Run lolight
  Open putty SSH or Terminal session then execute command below.

    cd ~/lolight
    ./lolight.py

If camera is working motion tracking logging information will be displayed.

## WebServer
Webserver.py will display saved motrack images from any network device using a web browser.

#### Foreground
To Run in Foreground open a new SSH or Terminal Session then execute command below.

    ./webserver.py

NOTE browser URL:PORT for accessing MoTrack web page will be displayed.  ctrl-c exits.

#### Background
To Run in Background execute command below in current SSH or Terminal Session. 
Then execute motrack.py in same terminal session per above.

    ./webserver.sh start

Access webserver with a web browser at provided URL and port  eg http://192.168.1.128:8090 or http://rpiname.local:8090

## More Info See

    https://github.com/pageauc/lolight

## Description

Takes timelapse images and saves in date name format to specified dirctory folder.
A video stream thread is run. Just before taking image a frame is read
from the video stream and the pixel average value is calculated using numpy.
This is compared to the darkness threshold DARK_START_PXAVE. Normally about 32 but
can be adjusted up or down. If the pxAve is below DARK_START_PXAVE then the camera
is put into low light mode. The exposure time in micro seconds is calculated.
Lower pxAve means higher exposure time up to the cameras maximum exposure time.
see getExposureSettings function below for details.

The video stream is stopped just before the timelapse image is taken, and
restarted after.  There is some error trapping to retry camera start if required.


