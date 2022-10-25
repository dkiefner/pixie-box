#!/bin/bash

# change locale to US
raspi-config nonint do_change_locale en_US.UTF-8

# enable SPI
raspi-config nonint do_spi 0

# update all os packages first
apt update
apt upgrade -y

# install python3 + pip
apt install -y python3-dev python3-pip

# install python spi module, rfid lib and text to speech lib
pip3 install spidev mfrc522 pyttsx3

# install mopidy + client & codecs
chmod +x ~/pixiebox/scripts/setup_audio.sh; ~/pixiebox/scripts/setup_audio.sh

# create needed directories
mkdir -p ~/pixiebox/data/audio/rfid
mkdir -p ~/pixiebox/data/audio/upload

# feedback that the installation is complete
python3 ~/pixiebox/scripts/install_complete_message.py
