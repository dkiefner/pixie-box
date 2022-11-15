#!/usr/bin/env python

import time

from lib.shutdown import Shutdown
from lib.store import ServiceStateStore


class SleepTimer:

    def __init__(self, service_state_store, player):
        self.service_state_store = service_state_store
        self.player = player

    def enable(self, timeout_in_seconds):
        self.service_state_store.save(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS, timeout_in_seconds)

    def disable(self):
        self.service_state_store.delete(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)

    def is_enabled(self):
        return self.service_state_store.get_string(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS) is not None

    def start_timer(self):
        player_stopped_timestamp = self.service_state_store.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)

        if player_stopped_timestamp is None:
            self.service_state_store.save(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP,
                                          str(self.__current_timestamp()))

    def is_running(self):
        return self.service_state_store.get_string(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP) is not None

    def stop_timer(self):
        if self.service_state_store.get_string(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP) is not None:
            self.service_state_store.delete(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)

    def is_sleep_timeout_reached(self):
        player_stopped_timestamp = self.service_state_store.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)
        sleep_timer_timeout = self.service_state_store.get_int(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)

        return self.__current_timestamp() - player_stopped_timestamp >= sleep_timer_timeout

    def get_timeout(self):
        timeout = self.service_state_store.get_string(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)
        return int(timeout) if not None else None

    def sleep(self):
        self.stop_timer()
        Shutdown.halt()

    @staticmethod
    def __current_timestamp():
        return int(time.time())
