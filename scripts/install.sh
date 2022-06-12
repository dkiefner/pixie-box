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

# install MPEG-4 AAC decoder to play mp3s
apt install -y gstreamer1.0-plugins-bad

# ensure the system audio settings match the user audio settings
ln -s ~/.asoundrc /etc/asound.conf

# Install mopidy
mkdir -p /usr/local/share/keyrings
wget -q -O /usr/local/share/keyrings/mopidy-archive-keyring.gpg https://apt.mopidy.com/mopidy.gpg
wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
apt update
apt install -y mopidy

# install mpd + client
apt install -y mopidy-mpd mpc

# configure mopidy (audio out and media folder)
echo "[audio]
output = alsasink

[file]
media_dirs =
  /home/pi/pixiebox/audio/
" > /etc/mopidy/mopidy.conf

# enable mopidy to run as a service, start it and print status
systemctl enable mopidy
systemctl start mopidy
systemctl status mopidy

# set volume to 65%
amixer set Headphone 65%
# play some sound to check if sound out works
aplay /usr/share/sounds/alsa/Front_Center.wav

# create directories needed
mkdir -p ~/pixiebox/audio/rfid
mkdir -p ~/pixiebox/audio/upload
