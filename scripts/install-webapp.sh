#!/bin/bash

# create a link for the service file to make the PixieBox Web App run using systemd
ln -s /home/pi/pixiebox/app/web/pixiebox_webapp.service /etc/systemd/system/pixiebox_webapp.service

# enable and start the PixieBox Web App service
systemctl daemon-reload
systemctl enable pixiebox_webapp.service
systemctl start pixiebox_webapp.service
