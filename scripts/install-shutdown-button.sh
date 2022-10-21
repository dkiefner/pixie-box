#!/bin/bash

# create a link for the service file to make the shutdown button script using systemd
ln -s /home/pi/pixiebox/backend/shutdown_system_with_button.service /etc/systemd/system/shutdown_system_with_button.service

# enable and start the shutdown system service
systemctl daemon-reload
systemctl enable shutdown_system_with_button.service
systemctl start shutdown_system_with_button.service
