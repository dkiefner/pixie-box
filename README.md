# PixieBox

An RFID based music player inspired by the [Phoniebox](https://github.com/MiczFlor/RPi-Jukebox-RFID).

## The Goal

The goal is to strip down the complex setup to very specific needs and requirements like:

- supports only playing local files for now
- supports only MFRC522 as an RFID scanner

## Hardware

- Raspberry Pi 4
- RC522 RFID reader (13.56 Mhz)
- Mifare RFID chips/tags (13.56 Mhz)

## Setup

### Raspberry Pi
#### When writing the Raspberry OS
- name the user `pi` as this will be used in most places of the service to reference resources
- install Raspberry Pi OS based on Debian Bullseye

#### After installing the Raspberry OS
One needs to change the following on the new boot partition:
- create a new ssh file in the root volume: `touch ssh`
- create a new `wpa_supplicant.conf` file in the root volume: `touch wpa_supplicant.conf`
- add the following content to the `wpa_supplicant.conf`:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=SE
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
```

### General

After installing the Pi OS and booting up the Pi, the following steps are needed:

**Download this repository:**  
One-time download:

```commandline
cd; wget https://github.com/dkiefner/pixiebox/archive/refs/heads/main.zip; unzip main.zip; rm main.zip; mv pixiebox-main pixiebox
```

Developer version (use `git pull` to get updates from latest `master`):

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

### Power LED

If you have an LED connected to the GPIO14 (TxD) then run the following script to enable the LED when the Pi is running:

```commandline
chmod +x ~/pixiebox/scripts/enable-power-led.sh; sudo ~/pixiebox/scripts/enable-power-led.sh
```

## Usage

### Create new RFID tags with audio

To create a new RFID tag and associate audio files with it, do the following:

- copy all audio files you want to play for a given RFID tag into `~/pixiebox/data/audio/upload` on the Raspberry Pi (
  e.g.
  using `scp` or share the directory using Samba)
- run the following script: `python3 ~/pixiebox/app/service/new_audio_tag.py` and it will do the magic

### Create new RFID tags with system actions

To link system actions like stopping the music to an RFID tag, run the following script:

```commandline
python3 ~/pixiebox/app/service/new_system_tag.py
```

### Run the player script and listen for RFID tags

For now, it is required to start the program manually (there will be a service setup provided soon):

```commandline
python3 ~/pixiebox/app/service/pixiebox.py
```

This will run the PixieBox in an endless loop. To stop it, press `Ctrl + C` (which will kill the current running script)
.

### Upload audio files to the upload folder of the PixieBox

A simple tool to do the job is `scp` to transfer files from a Computer to the PixieBox. Here is an example to move all
audio files from `~/Downloads/pixiebox-audio` on a Computer to the upload folder of the PixieBox. Please
replace `<pi-user>` with the actual username you used to set up the Raspberry Pi (usually this is `pi`) and `<pi-ip>`
with the ip address of the Raspberry Pi in the local network (e.g. `192.168.0.1`):

```commandline
scp -r ~/Downloads/pixiebox-audio <pi-user>@<pi-ip>:~/pixiebox/data/audio/upload/
```

Note: It is important to use the `-r` parameter to move every file in a directory to its destination as all as having
no `/` at the end of the first path. Adding a `/` would transfer the folder instead of all the files within that folder.

### Run as a service

The PixieBox reader can be run as a service in the background. If enabled, it will also make sure the service is up and
running after every restart of the Pi.

#### Install the service

To install and start the service as a systemd service, run the following command:

```commandline
chmod +x ~/pixiebox/scripts/install-service.sh; sudo ~/pixiebox/scripts/install-service.sh
```

After executing the script, run the following command to check if service is up and running:

```commandline
sudo systemctl status pixiebox.service
```

This should print something like the following:

```commandline
● pixiebox.service - PixieBox music player service
     Loaded: loaded (/home/pi/pixiebox/app/service/pixiebox.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-08-02 12:51:08 CEST; 6min ago
   Main PID: 1299 (python3)
      Tasks: 1 (limit: 4164)
        CPU: 6min 38.289s
     CGroup: /system.slice/pixiebox.service
             └─1299 /usr/bin/python3 /home/pi/pixiebox/app/service/pixiebox.py
```

The important part to look for in the output is `Active: active (running)`.

#### Start and stop the service

The service can be stopped and started manually. This is needed if one want to run other scripts that want to use the
RFID reader like create a new tag. Remember to start teh service again after you finished with the other script.

To stop the service run the following command:

```commandline
sudo systemctl stop pixiebox.service
```

To start the service run:

```commandline
sudo systemctl start pixiebox.service
```

#### Service logs

When running the PixieBox as a service, all stdout and stderr will be logged to the journal instead of the terminal.

To see the journal logs, run the following command:

```commandline
sudo journalctl --unit=pixiebox
```

To see live updates of the journal, add the parameter `-f` to "follow" the log.

### Install a system shutdown button

To use a button for turning the Raspberry Pi on and off, wire the button up on `GPIO3` and `GND`. Turning on the
Raspberry Pi will be handled by the Raspberry Pi itself, there is no more work needed. To turn the Raspberry Pi off a
software solution is necessary. Even though the Raspberry PI is shutdown properly, the red light on the Raspberry Pi is
still on. The red light only indicates that the Raspberry Pi is receiving enough power.

#### Install the service

To install and start a service that is listening for the button press, run the following command:

```commandline
chmod +x ~/pixiebox/scripts/install-shutdown-button.sh; sudo ~/pixiebox/scripts/install-shutdown-button.sh
```

After executing the script, run the following command to check if service is up and running:

```commandline
sudo systemctl status shutdown_system_with_button.service
```

This should print something like the following:

```commandline
● shutdown_system_with_button.service - Shutdown the system on button press
     Loaded: loaded (/home/pi/pixiebox/app/service/shutdown_system_with_button.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2022-10-21 20:57:17 CEST; 17s ago
   Main PID: 964 (python3)
      Tasks: 1 (limit: 4164)
        CPU: 61ms
     CGroup: /system.slice/shutdown_system_with_button.service
             └─964 /usr/bin/python3 -u /home/pi/pixiebox/app/service/shutdown_system_with_button.py

Oct 21 20:57:17 raspberrypi systemd[1]: Started Shutdown the system on button press.
Oct 21 20:57:17 raspberrypi python3[964]: Waiting for button press...
```

The important part to look for in the output is `Active: active (running)`.

### Install the Web App

The Web App simplifies some administration like attaching audio to RFID tags, creating backups or controlling the media player.

#### Install the service

To install and start the service that is running the Web App, run the following command:

```commandline
chmod +x ~/pixiebox/scripts/install-webapp.sh; sudo ~/pixiebox/scripts/install-webapp.sh
```

After executing the script, run the following command to check if service is up and running:

```commandline
sudo systemctl status pixiebox_webapp.service
```

This should print something like the following:

```commandline
● pixiebox_webapp.service - Web app for PixieBox music player
     Loaded: loaded (/home/pi/pixiebox/app/web/pixiebox_webapp.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-11-08 19:57:42 CET; 42s ago
   Main PID: 978 (python3)
      Tasks: 1 (limit: 4164)
        CPU: 531ms
     CGroup: /system.slice/pixiebox_webapp.service
             └─978 /usr/bin/python3 -u -m flask --app=/home/pi/pixiebox/app/web/app run --host=0.0.0.0

Nov 08 19:57:42 raspberrypi systemd[1]: Started Web app for PixieBox music player.
Nov 08 19:57:42 raspberrypi python3[978]:  * Serving Flask app '/home/pi/pixiebox/app/web/app'
Nov 08 19:57:42 raspberrypi python3[978]:  * Debug mode: off
Nov 08 19:57:42 raspberrypi python3[978]: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
Nov 08 19:57:42 raspberrypi python3[978]:  * Running on all addresses (0.0.0.0)
Nov 08 19:57:42 raspberrypi python3[978]:  * Running on http://127.0.0.1:5000
Nov 08 19:57:42 raspberrypi python3[978]:  * Running on http://192.168.0.20:5000
Nov 08 19:57:42 raspberrypi python3[978]: Press CTRL+C to quit
```

The important part to look for in the output is `Active: active (running)`.

## The Result

![GPIO Setup](https://github.com/dkiefner/pixiebox/blob/main/docs/resources/gpio.jpg?raw=true)
![GPIO Setup](https://github.com/dkiefner/pixiebox/blob/main/docs/resources/lower.jpg?raw=true)
![GPIO Setup](https://github.com/dkiefner/pixiebox/blob/main/docs/resources/upper.jpg?raw=true)
