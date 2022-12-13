#!/usr/bin/env python

import time

from lib.logger import Logger
from lib.store import ServiceStateStore


class SleepTimer:

    def __init__(self, service_state_store, player, shutdown):
        self.service_state_store = service_state_store
        self.player = player
        self.shutdown = shutdown

    def enable(self, timeout_in_seconds):
        Logger.log("Sleep timer enabled")
        self.service_state_store.save(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS, timeout_in_seconds)

    def disable(self):
        Logger.log("Sleep timer disabled")
        self.service_state_store.delete(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)

    def is_enabled(self):
        return self.service_state_store.get_string(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS) is not None

    def is_running(self):
        return self.service_state_store.get_string(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP) is not None

    def is_sleep_timeout_reached(self):
        player_stopped_timestamp = self.service_state_store.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)
        sleep_timer_timeout = self.service_state_store.get_int(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)
        current_timestamp = self.__current_timestamp()
        time_left = (player_stopped_timestamp + sleep_timer_timeout) - current_timestamp

        Logger.log(
            f"Check if sleep timeout is reached: current_time={current_timestamp} "
            f"player_stopped_time={player_stopped_timestamp} timeout={sleep_timer_timeout} time_left={time_left}")

        return current_timestamp - player_stopped_timestamp >= sleep_timer_timeout

    # If the timeout time is less than 0, the cleanup failed while stopping or starting the sleep timer service.
    # This means we have a very old stopped time and the Pixiebox would shut down ~15s after startup
    # (because the sleep timeout has been reached).
    # -3s because the Raspberry Pi needs ~30s to boot + 15s initial sleep timeout
    def is_valid(self):
        player_stopped_timestamp = self.service_state_store.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)
        sleep_timer_timeout = self.service_state_store.get_int(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)
        current_timestamp = self.__current_timestamp()
        time_left = (player_stopped_timestamp + sleep_timer_timeout) - current_timestamp

        return time_left < -30

    def start_timer(self):
        player_stopped_timestamp = self.service_state_store.get_int(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)

        if player_stopped_timestamp is None:
            Logger.log("Sleep timer started")
            self.service_state_store.save(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP,
                                          str(self.__current_timestamp()))

    def stop_timer(self):
        if self.service_state_store.get_string(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP) is not None:
            Logger.log("Sleep timer stopped")
            self.service_state_store.delete(ServiceStateStore.KEY_PLAYER_STOPPED_TIMESTAMP)

    def get_timeout(self):
        timeout = self.service_state_store.get_string(ServiceStateStore.KEY_SLEEP_TIMER_TIMEOUT_IN_SECONDS)

        if timeout is not None:
            return int(timeout)
        else:
            return None

    def sleep(self):
        self.stop_timer()
        self.shutdown.halt()

    @staticmethod
    def __current_timestamp():
        return int(time.time())
