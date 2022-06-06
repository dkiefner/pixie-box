#!/bin/bash

echo "Playing test music..."

mpc -q clear
mpc add file:///home/pi/pixiebox/audio/system/late-jazz-piano.wav
mpc -q play

echo "Playing test music done."
