#!/usr/bin/env python

import time

from lib.player import LocalFilePlayer
from lib.shutdown import Shutdown
from lib.store import ServiceStateStore

KEY_SLEEP_TIMER_TIME_IN_SECONDS = "sleep_timer_time_in_seconds"
KEY_PLAYER_STOPPED_TIMESTAMP = "player_stopped_timestamp"

serviceStateStore = ServiceStateStore()
player = LocalFilePlayer(serviceStateStore)


def is_enabled():
    return serviceStateStore.get_string(KEY_SLEEP_TIMER_TIME_IN_SECONDS) is not None


def reset_timer():
    if serviceStateStore.get_string(KEY_PLAYER_STOPPED_TIMESTAMP) is not None:
        serviceStateStore.delete(KEY_PLAYER_STOPPED_TIMESTAMP)


def current_timestamp():
    return int(time.time())


def is_sleep_timeout_reached():
    return current_timestamp() - serviceStateStore.get_int(KEY_PLAYER_STOPPED_TIMESTAMP) >= serviceStateStore.get_int(
        KEY_SLEEP_TIMER_TIME_IN_SECONDS)


def start_timer():
    player_stopped_timestamp = serviceStateStore.get_int(KEY_PLAYER_STOPPED_TIMESTAMP)

    if player_stopped_timestamp is None:
        serviceStateStore.save(KEY_PLAYER_STOPPED_TIMESTAMP, str(current_timestamp()))
    else:
        if is_sleep_timeout_reached():
            Shutdown.halt()


while True:
    if is_enabled():
        if player.is_playing():
            reset_timer()
        else:
            start_timer()

    # Check every 10 seconds if we should shut down
    time.sleep(10)
