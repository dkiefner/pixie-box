# pixie-box
An RFID based music player inspired by the [Phoniebox](https://github.com/MiczFlor/RPi-Jukebox-RFID).

## The Goal
The goal is to strip down the complex setup to very specific needs and requirements like:
- supports only playing local files for now
- supports only MFRC522 as an RFID scanner

## Hardware
- Raspberry Pi (3/4)
- RC522 RFID reader (13.56 Mhz)
- Mifare RFID chips/tags (13.56 Mhz)

## Setup
After installing the Pi OS and booting up the pi, the following steps are needed:

Install Git:
```commandline
sudo apt install -y git
```

Clone this repository (preferably into your home folder):
```commandline
git clone git@github.com:dkiefner/pixie-box.git
```

Run the installation script:
```commandline
~/pixie-box/scripts/install.sh
```

## Usage
For now, it is required to start the program manually (there will be a service setup provided soon):
```commandline
python3 ~/pixie-box/src/pixiebox.py
```

This will run the Pixie-Box in an endless loop. To stop it, press `Ctrl + C` (which will kill the current running script).
