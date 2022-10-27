#!/bin/bash

# create a link for the service file to make the PixieBox reader run using systemd
ln -s /home/pi/pixiebox/app/service/pixiebox.service /etc/systemd/system/pixiebox.service

# enable and start the PixieBox reader service
systemctl daemon-reload
systemctl enable pixiebox.service
systemctl start pixiebox.service
