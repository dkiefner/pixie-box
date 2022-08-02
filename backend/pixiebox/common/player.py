#!/usr/bin/env python

from common.logger import Logger
from common.shell import Shell


class SystemAudioUris:
    SAD_TROMBONE = "file:///home/pi/pixiebox/audio/system/sad-trombone.wav"


class Player:
    def play_rfid(self, tag_id):
        Logger.log(f"Playing RFID tag {tag_id}")

    def play_file(self, file_uri):
        Logger.log(f"Playing file {file_uri}")

    def stop(self):
        Logger.log(f"Stop playing")


class LocalFilePlayer(Player):
    KEY_LAST_PLAYED_URI = "last-played-uri"
    VOLUME_MIN_VALUE = 10
    VOLUME_MAX_VALUE = 100
    VOLUME_CHANGE_VALUE = 10

    def __init__(self, service_state_store):
        self.service_state_store = service_state_store

    def play_rfid(self, tag_id):
        uri = self.tag_id_to_uri(tag_id)
        super().play_rfid(uri)
        self.__play(uri)

    @staticmethod
    def tag_id_to_uri(tag_id):
        return f"Files/rfid/{tag_id}"

    def play_file(self, file_uri):
        super().play_file(file_uri)
        self.__play(file_uri)

    def __play(self, uri):
        Shell.execute("mpc -q clear")
        Shell.execute(f"mpc -q add {uri}")
        Shell.execute("mpc -q play")
        self.service_state_store.save(self.KEY_LAST_PLAYED_URI, uri)

    def stop(self):
        Shell.execute("mpc -q stop")

    def volume_up(self):
        current = self.__get_volume()
        Logger.log(f"Increase volume. Current level is {current}%")

        if current < self.VOLUME_MAX_VALUE:
            if (current + self.VOLUME_CHANGE_VALUE) > self.VOLUME_MAX_VALUE:
                self.__set_volume(self.VOLUME_MAX_VALUE)
            else:
                self.__set_volume(current + self.VOLUME_CHANGE_VALUE)
        else:
            Logger.log("Cannot increase volume. Maximum volume reached.")

    def volume_down(self):
        current = self.__get_volume()
        Logger.log(f"Decrease volume. Current level is {current}%")

        if current > self.VOLUME_MIN_VALUE:
            if (current - self.VOLUME_CHANGE_VALUE) < self.VOLUME_MIN_VALUE:
                self.__set_volume(self.VOLUME_MIN_VALUE)
            else:
                self.__set_volume(current - self.VOLUME_CHANGE_VALUE)
        else:
            Logger.log(f"Cannot decrease volume. Minimum volume level of {self.VOLUME_MIN_VALUE}% reached.")

    @staticmethod
    def __get_volume():
        level = Shell.execute(
            "amixer sget Headphone | awk -F 'Playback|[][]' 'BEGIN {RS=\"\"}{ print substr($5, 1, length($5)-1) }'")
        return int(level)

    @staticmethod
    def __set_volume(level):
        if 0 <= level <= 100:
            Shell.execute(f"amixer set Headphone {level}%")
        else:
            Logger.log(f"Invalid volume of [{level}]. The volume level needs to be between 0 and 100.")

    @staticmethod
    def is_playing():
        current = Shell.execute("mpc current")

        return len(current) > 0

    def is_playing_tag(self, tag_id):
        return self.is_playing() and self.tag_id_to_uri(tag_id) is self.get_last_played_uri()

    def get_last_played_uri(self):
        return self.service_state_store.get(self.KEY_LAST_PLAYED_URI)
