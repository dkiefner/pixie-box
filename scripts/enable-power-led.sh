#!/bin/bash

# Disable login shell over serial and enable serial port
raspi-config nonint do_serial 2
