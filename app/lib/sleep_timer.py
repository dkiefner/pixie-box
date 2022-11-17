#!/usr/bin/env python

import time

from lib.logger import Logger
from lib.shutdown import Shutdown
from lib.store import ServiceStateStore


class SleepTimer:

    def __init__(self, service_state_store, player):
        self.service_state_store = service_state_store
        self.player = player

    def enable(self, timeout_in_seconds):
        Logger.log("Sleep timer enabled")
        self.service_state_store.save(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS, timeout_in_seconds)

    def disable(self):
        Logger.log("Sleep timer disabled")
        self.service_state_store.delete(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)

    def is_enabled(self):
        return self.service_state_store.get_string(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS) is not None

    def start_timer(self):
        player_stopped_timestamp = self.service_state_store.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)

        if player_stopped_timestamp is None:
            Logger.log("Sleep timer started")
            self.service_state_store.save(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP,
                                          str(self.__current_timestamp()))

    def is_running(self):
        return self.service_state_store.get_string(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP) is not None

    def stop_timer(self):
        if self.service_state_store.get_string(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP) is not None:
            Logger.log("Sleep timer stopped")
            self.service_state_store.delete(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)

    def is_sleep_timeout_reached(self):
        player_stopped_timestamp = self.service_state_store.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)
        sleep_timer_timeout = self.service_state_store.get_int(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)
        current_timestamp = self.__current_timestamp()

        Logger.log(
            f"Check if sleep timeout is reached: current_time={current_timestamp} "
            f"player_stopped_time={player_stopped_timestamp} timeout={sleep_timer_timeout}")

        return current_timestamp - player_stopped_timestamp >= sleep_timer_timeout

    def get_timeout(self):
        timeout = self.service_state_store.get_string(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)

        if timeout is not None:
            return int(timeout)
        else:
            return None

    def sleep(self):
        self.stop_timer()
        Shutdown.halt()

    @staticmethod
    def __current_timestamp():
        return int(time.time())
