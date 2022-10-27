# A collection of some helper commands when dealing with this project

## Mopidy
See Mopidy logs:
```commandline
sudo journalctl -u mopidy
```

Restart Mopidy service:
```commandline
sudo systemctl restart mopidy
```

## MPC
List all MPD resources:
```commandline
mpc ls
```

List all MPD targets in a resource (e.g. Files):
```commandline
mpc list "Files"
```

Add a target to the current playlist (e.g. test-music.wav):
```commandline
mpc list add file:///home/pi/pixiebox/audio/system/test-music.wav
```

Control the MPD player:
```commandline
mpc play
mpc stop
mpc current
```

For more MPC commands see the [official man page](https://linux.die.net/man/1/mpc)
