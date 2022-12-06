#!/usr/bin/env python

from lib.file_system import FileSystem
from lib.logger import Logger
from lib.shell import Shell


class SystemAudioUris:
    SAD_TROMBONE = f"file://{FileSystem.SYSTEM_AUDIO_DIR}sad-trombone.wav"
    GAME_BOY_START_UP = f"file://{FileSystem.SYSTEM_AUDIO_DIR}game-boy-startup.wav"


class Player:
    def play_rfid(self, tag_id):
        Logger.log(f"Playing RFID tag {tag_id}")

    def play_file(self, file_uri):
        Logger.log(f"Playing file {file_uri}")

    def stop(self):
        Logger.log("Stop playing")

    def next(self):
        pass

    def prev(self):
        pass

    def is_playing(self, uri=None):
        pass

    def get_last_played_uri(self):
        pass


class LocalFilePlayer(Player):
    KEY_LAST_PLAYED_URI = "last-played-uri"

    def __init__(self, service_state_store):
        self.service_state_store = service_state_store

    def play_rfid(self, tag_id):
        uri = self.__tag_id_to_uri(tag_id)
        super().play_rfid(uri)
        self.__play(uri)

    @staticmethod
    def __tag_id_to_uri(tag_id):
        return f"Files/rfid/{tag_id}"

    def play_file(self, file_uri):
        super().play_file(file_uri)
        self.__play(file_uri)

    def __play(self, uri):
        if self.is_playing(uri=uri):
            Logger.log("The current context is already playing.")
        else:
            Shell.execute("mpc -q clear")
            Shell.execute(f"mpc -q add {uri}")
            Shell.execute("mpc -q play")
            self.service_state_store.save(self.KEY_LAST_PLAYED_URI, uri)

    def stop(self):
        Shell.execute("mpc -q stop")

    def next(self):
        Shell.execute("mpc -q next")

    def prev(self):
        Shell.execute("mpc -q prev")

    def is_playing(self, uri=None):
        current = Shell.execute("mpc current")
        is_playing = len(current) > 0
        Logger.log(f"Is playing any context: {is_playing}")

        if uri is None:
            return is_playing
        else:
            last_played_uri = self.get_last_played_uri()
            Logger.log(f"Is playing uri={uri} (last_played_uri={last_played_uri})")
            return is_playing and uri == last_played_uri

    def get_last_played_uri(self):
        return self.service_state_store.get_string(self.KEY_LAST_PLAYED_URI)


class FakePlayer(Player):
    def play_rfid(self, tag_id):
        Logger.log(f"Playing RFID tag {tag_id}")

    def play_file(self, file_uri):
        Logger.log(f"Playing file {file_uri}")

    def stop(self):
        Logger.log("Stop playing")

    def next(self):
        Logger.log("Playing next")

    def prev(self):
        Logger.log("Playing previous")

    def is_playing(self, uri=None):
        return False

    def get_last_played_uri(self):
        return None
