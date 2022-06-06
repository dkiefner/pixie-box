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
chmod +x ~/pixiebox/scripts/install.sh; sudo ~/pixiebox/scripts/install.sh
```

Test if everything is set up correct (hint: you should hear piano music playing):
```commandline
chmod +x ~/pixiebox/scripts/test-setup.sh; ~/pixiebox/scripts/test-setup.sh
```

## Usage

### Create new RFID tags with audio
To create a new RFID tag and associate audio files with it, do the following:
- copy all audio files into `~/pixiebox/audio/upload` on teh Raspberry Pi (e.g. using `scp`)
- run the following script: `python3 ~/pixiebox/scripts/new_tag.py`

### Run the player script and listen for RFID tags
For now, it is required to start the program manually (there will be a service setup provided soon):
```commandline
python3 ~/pixiebox/src/pixiebox.py
```

This will run the PixieBox in an endless loop. To stop it, press `Ctrl + C` (which will kill the current running script).
