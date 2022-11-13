#!/usr/bin/env python

import time

from lib.player import LocalFilePlayer
from lib.shutdown import Shutdown
from lib.store import ServiceStateStore

serviceStateStore = ServiceStateStore()
player = LocalFilePlayer(serviceStateStore)


def is_enabled():
    return serviceStateStore.get_string(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS) is not None


def reset_timer():
    if serviceStateStore.get_string(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP) is not None:
        serviceStateStore.delete(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)


def current_timestamp():
    return int(time.time())


def is_sleep_timeout_reached():
    player_stopped_timestamp = serviceStateStore.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)
    sleep_timer_timeout = serviceStateStore.get_int(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)

    return current_timestamp() - player_stopped_timestamp >= sleep_timer_timeout


def start_timer():
    player_stopped_timestamp = serviceStateStore.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)

    if player_stopped_timestamp is None:
        serviceStateStore.save(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP, str(current_timestamp()))
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
