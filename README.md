# PixieBox
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
After installing the Pi OS and booting up the Pi, the following steps are needed:

Download this repository:
```commandline
cd; wget https://github.com/dkiefner/pixiebox/archive/refs/heads/main.zip; unzip main.zip; rm main.zip; mv pixiebox-main pixiebox
```

Run the installation script:
```commandline
~/pixiebox/scripts/install.sh
```

## Usage
For now, it is required to start the program manually (there will be a service setup provided soon):
```commandline
python3 ~/pixiebox/src/pixiebox.py
```

This will run the PixieBox in an endless loop. To stop it, press `Ctrl + C` (which will kill the current running script).
