# lolight.py Create Low Light Timelapse Images
## written by Claude Pageau

## Intro
Written as a test/learning program to help convert pi-timolo https://github.com/pageauc/pi-timolo
to use the picamera2 python module.
Different methods were tried for automating settings for low light/day light timelapse images.
This program was useful for trying and testing differnt ideas.
I cleaned it up a bit and will post on GitHub to share with others who may find it useful.

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


