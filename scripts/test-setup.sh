#!/bin/bash

echo "Playing test music..."
echo "run \"mpc stop\" to stop the music"
mpc -q clear
mpc add file:///home/pi/pixiebox/audio/system/test-music.wav
mpc -q play
