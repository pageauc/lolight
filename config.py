
# User Settings for lolight.py
# ============================

# Image Settings
# --------------
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

# Web Server settings
# -------------------
WEB_SERVER_PORT = 8090        # Default= 8090 Web server access port eg http://192.168.1.100:8080
WEB_SERVER_ROOT = "media"     # Default= "media" webserver root path to webserver image/video su>
WEB_PAGE_TITLE = "PI-TIMOLO2" # web page title that browser show (not displayed on web page)
WEB_PAGE_REFRESH_ON = True    # False=Off (never)  Refresh True=On (per seconds below)
WEB_PAGE_REFRESH_SEC = "900"  # Default= "900" seconds to wait for web page refresh  seconds (15>
WEB_PAGE_BLANK_ON = False     # True Starts left image with a blank page until a right menu item>
                              # False displays second list[1] item since first may be in progress

# Left iFrame Image Settings
# --------------------------
WEB_IMAGE_HEIGHT = "768"       # Default= "768" px height of images to display in iframe
WEB_IFRAME_WIDTH_PERCENT = "70%" # Left Pane - Sets % of total screen width allowed for iframe. >
WEB_IFRAME_WIDTH = "100%"      # Desired frame width to display images. can be eg percent "80%" >
WEB_IFRAME_HEIGHT = "100%"     # Desired frame height to display images. Scroll bars if image la>

# Right Side Files List
# ---------------------
WEB_MAX_LIST_ENTRIES = 0           # 0 = All or Specify Max right side file entries to show (mus>
WEB_LIST_HEIGHT = WEB_IMAGE_HEIGHT # Right List - side menu height in px (link selection)
WEB_LIST_BY_DATETIME_ON = True     # True=datetime False=filename
WEB_LIST_SORT_DESC_ON = True       # reverse sort order (filename or datetime per web_list_by_da>

# ---------------------------------------------- End of User Variables -----------------------------------------------------
