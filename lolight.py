#!/usr/bin/env python3
from __future__ import print_function
"""
Written as a test/learning program to help convert pi-timolo https://github.com/pageauc/pi-timolo
to use the picamera2 python module.
Different methods were tried for automating settings for low light/day light timelapse images.
This program was useful for trying and testing differnt ideas.
I cleaned it up a bit and will post on GitHub to share with others who may find it useful.

Description

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

"""
PROG_VER = 'ver 1.0'
import os
PROG_NAME = os.path.basename(__file__)
print(f'{PROG_NAME} {PROG_VER} written by Claude Pageau  Loading ...\n')
# import required python libraries
from picamera2 import Picamera2
from libcamera import controls, Transform
import sys
import time
import datetime
from strmpilibcam import CamStream
import numpy as np

# User Settings
# =============

# Image Settings
IM_TIMELAPSE_DELAY_SEC = 120
IM_PREFIX = "LO-"    # File name prefix
IM_W = 1920   
IM_H = 1080
IM_FORMAT = ".jpg"   # Default= ".jpg"  other Formats .jpeg .png .gif .bmp 
IM_VFLIP = True  # flip image vertically    
IM_HFLIP = True  # flip image horizontally  Decided not to use rotate.
IM_DIR = 'media/lowlight/'  # directory to save images (add trailing forward slash

# Low Light Settings
DARK_MAX_EXP_SEC = 5.9   # picamera V1 default is 6.0 sec. V2 is 10 Sec
DARK_START_PXAVE = 32    # pxAve transition point between dark and light.
DARK_GAIN = 10.0         # analogue_gain (ISO/100) for dark mode.  Max is 16
# End User Settings

# Constants
SEC_TO_MICROSEC = 1000000     # 1 second=10000000 microseconds

if DARK_GAIN > 16:
    DARK_GAIN = 16


# ------------------------------------------------------------------------------
def makeDirs(dirPath='media/images'):
    if not os.path.isdir(dirPath):
        print(f"Create Folder {dirPath}")
        try:
            os.makedirs(dirPath)
        except OSError as err:
            print(f"Could Not Create {dirPath} {err}")
            sys.exit(1)


# ------------------------------------------------------------------------------
def getStreamPixAve(streamData):
    """
    Calculate the average pixel values for the specified stream
    used for determining day/night or twilight conditions
    """
    pixAverage = int(np.average(streamData[..., 1]))  # Use 0=red 1=green 2=blue
    return pixAverage


# ------------------------------------------------------------------------------
def getExposureSettings(pxAve):
    """ 
    Use the pxAve and DARK_START_PXAVE threshold to set
    analogue_gain for day or darkness
    """
    if pxAve > DARK_START_PXAVE:
        exposure_microsec = 0    # Auto
        analogue_gain = 0        # Auto
    else:
        exposure_sec = DARK_MAX_EXP_SEC / DARK_START_PXAVE
        exposure_microsec = int(exposure_sec * (DARK_START_PXAVE - pxAve) * SEC_TO_MICROSEC)
        analogue_gain = DARK_GAIN
    return exposure_microsec, analogue_gain


# ------------------------------------------------------------------------------
def getImageFilename(path, prefix, pxAve):
    """build image file names by number sequence or date/time"""
    rightNow = datetime.datetime.now()
    filename = "%s%s%s-%04d-%02d-%02d_%02d:%02d:%02d%s" % (
        path,
        prefix,
        str(pxAve),
        rightNow.year,
        rightNow.month,
        rightNow.day,
        rightNow.hour,
        rightNow.minute,
        rightNow.second,
        IM_FORMAT
    )
    return filename


# ------------------------------------------------------------------------------
def takeImage(filepath, im_data):
    """
    Get camera settings, configure camera for dark or bright conditions based on pxAve
    Take and save still image
    """
    pxAve = getStreamPixAve(im_data)
    exposure_microsec, analogue_gain = getExposureSettings(pxAve)
    retries = 0
    total_retries = 3
    while retries < total_retries:
        try:
            picam2 = Picamera2()  # Initialize the camera
            config = picam2.create_preview_configuration({"size": (IM_W, IM_H)},
                                                          transform=Transform(vflip=IM_VFLIP,
                                                                              hflip=IM_HFLIP))
            picam2.configure(config)
        except RuntimeError:
            retries += 1
            print('Camera Error. Could Not Configure')
            print(f'Retry {retries} of {total_retries}')
            picam2.close()  # Close the camera instance
            if retries > total_retries:
                print('Retries Exceeded. Exiting Due to Camera Problem. ')
                sys.exit(1)
            else:
                time.sleep(4)
                continue
        break
    picam2.set_controls({"ExposureTime": exposure_microsec,
                         "AnalogueGain": analogue_gain,
                         "FrameDurationLimits": (exposure_microsec, exposure_microsec)})

    # picam2.set_controls({"ExposureTime": exposure_microsec, "AnalogueGain": analogue_gain})
    picam2.start()  # Start the camera instance

    # Allow some time for the camera to adjust to the light conditions
    if analogue_gain < 1:  # set for daylight. Auto is 0
        time.sleep(4) # Allow time for camera warm up
    else:
        print(f'Low Light {pxAve}/{DARK_START_PXAVE} pxAve')
        time.sleep(DARK_GAIN) # Allow time for camera to adjust for long exposure

    print(f"ImageSize=({IM_W}x{IM_H}) vflip={IMAGE_VFLIP} hflip={IMAGE_HFLIP}")
    print(f"pxAve={pxAve}, Exposure={exposure_microsec} microsec, Gain={analogue_gain} Auto is 0")
    print(f"Save Image to {filepath}")
    picam2.capture_file(filepath)      # Capture the image
    picam2.close()  # Close the camera instance


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    makeDirs(IM_DIR) # create directories if they do not exist
    try:
        while True:
            print('INFO  : Start Video Stream Thread')
            vs = CamStream(size=(320, 240),
                   vflip=True,
                   hflip=True).start()
            print('INFO  : Video Stream Thread is Running.')                   
            print(f'INFO  : Waiting {IM_TIMELAPSE_DELAY_SEC} seconds for Next Timelapse')
            print('        Press Ctrl-c to Exit')
            time.sleep(IM_TIMELAPSE_DELAY_SEC)
            print('INFO  : Read a Video Stream Frame for pxAve Calculation')
            im_data = vs.read()
            print('INFO  : Stop Video Stream Thread')
            vs.stop()
            filepath = getImageFilename(IM_DIR, IM_PREFIX, pxAve)
            takeImage(filepath, im_data)
    except KeyboardInterrupt:
        print('\nUser Pressed Ctrl-C to Exit')
    finally:
        vs.stop()
        print(f'{PROG_NAME} {PROG_VER} Bye ...')


