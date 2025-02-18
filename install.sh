#!/bin/bash
echo "lolight Install written by Claude Pageau"
cd ~
mkdir -p lolight
cd lolight
mkdir -p media

echo "INFO  : Download Project Files ..."
wget -O lolight.py -q --show-progress https://raw.github.com/pageauc/lolight/master/lolight.py
wget -O lolight.sh -q --show-progress https://raw.github.com/pageauc/lolight/master/lolight.sh
wget -O webserver.py -q --show-progress https://raw.github.com/pageauc/lolight/master/webserver.py
wget -O webserver.sh -q --show-progress https://raw.github.com/pageauc/lolight/master/webserver.sh
wget -O strmpilibcam.py -q --show-progress https://raw.github.com/pageauc/lolight/master/strmpilibcam.py
wget -O Readme.md -q --show-progress https://raw.github.com/pageauc/lolight/master/Readme.md
wget -O media/webserver.txt -q --show-progress https://raw.github.com/pageauc/lolight/master/webserver.txt

if [ -f config.py ]; then     # check if local file exists.
    wget -O config.py.new -q --show-progress https://raw.github.com/pageauc/lolight/master/config.py
else
    wget -O config.py -q --show-progress https://raw.github.com/pageauc/lolight/master/config.py
fi

chmod +x lolight.py webserver.py webserver.sh

echo "INFO  : Install Dependencies ...."


echo "
                    INSTRUCTIONS
                    ============
How to Run
==========
In SSH or Terminal session
Edit config.py lolight settings

    cd ~/lolight
    ./lolight.py

EDIT SETTINGS
=============

    nano config.py

To exit and save settings. In nano press

    ctrl-x then y

RUN WEBSERVER
=============

Run Web in Foreground open a new terminal (Displays browser URL)

    ./webserver.py

Run in Background in existing terminal

    ./webserver.sh start

Access webserver with a web browser at URL per Foreground command.

Form More Info See https://github.com/pageauc/lolight
"

