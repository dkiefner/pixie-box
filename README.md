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

**Download this repository:**  
One-time download:

```commandline
cd; wget https://github.com/dkiefner/pixiebox/archive/refs/heads/main.zip; unzip main.zip; rm main.zip; mv pixiebox-main pixiebox
```

Developer version (to use `git pull` to get updates from latest `master`):

```commandline
cd; sudo apt install -y git; git clone https://github.com/dkiefner/pixiebox.git
```

**Run the installation script:**

```commandline
chmod +x ~/pixiebox/scripts/install.sh; sudo ~/pixiebox/scripts/install.sh
```

**Test if everything is set up correct (hint: you should hear piano music playing):**

```commandline
chmod +x ~/pixiebox/scripts/test-setup.sh; ~/pixiebox/scripts/test-setup.sh
```

## Usage

### Create new RFID tags with audio

To create a new RFID tag and associate audio files with it, do the following:

- copy all audio files you want to play for a given RFID tag into `~/pixiebox/audio/upload` on the Raspberry Pi (e.g.
  using `scp` or share the directory using Samba)
- run the following script: `python3 ~/pixiebox/backend/pixiebox/new_audio_tag.py` and it will do the magic

### Create new RFID tags with system actions

To link system actions like stopping the music to an RFID tag, run the following script:

```commandline
python3 ~/pixiebox/backend/pixiebox/new_system_tag.py
```

### Run the player script and listen for RFID tags

For now, it is required to start the program manually (there will be a service setup provided soon):

```commandline
python3 ~/pixiebox/backend/pixiebox/pixiebox.py
```

This will run the PixieBox in an endless loop. To stop it, press `Ctrl + C` (which will kill the current running script)
.

### Upload audio files to the upload folder of the PixieBox

A simple tool to do the job is `scp` to transfer files from a Computer to the PixieBox. Here is an example to move all
audio files from `~/Downloads/pixiebox-audio` on a Computer to the upload folder of the PixieBox. Please
replace `<pi-user>` with the actual username you used to set up the Raspberry Pi (usually this is `pi`) and `<pi-ip>`
with the ip address of the Raspberry Pi in the local network (e.g. `192.168.0.1`):

```commandline
scp -r ~/Downloads/pixiebox-audio <pi-user>@<pi-ip>:~/pixiebox/audio/upload/
```

Note: It is important to use the `-r` parameter to move every file in a directory to its destination as all as having
no `/` at the end of the first path. Adding a `/` would transfer the folder instead of all the files within that folder.
