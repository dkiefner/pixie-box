#!/bin/bash

## Main service to play audio ##
# create a link for the service file to make the PixieBox reader run using systemd
ln -s /home/pi/pixiebox/app/service/pixiebox.service /etc/systemd/system/pixiebox.service

# enable and start the PixieBox reader service
systemctl daemon-reload
systemctl enable pixiebox.service
systemctl start pixiebox.service


## Sleep timer service ##
# create a link for the service file to make the sleep timer run using systemd
ln -s /home/pi/pixiebox/app/service/sleep_timer.service /etc/systemd/system/sleep_timer.service

# enable and start the sleep timer service
systemctl daemon-reload
systemctl enable sleep_timer.service
systemctl start sleep_timer.service
