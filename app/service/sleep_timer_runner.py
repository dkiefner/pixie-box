#!/usr/bin/env python

import time

from lib.di import ServiceLocatorFactory, ServiceName
from lib.logger import Logger
from lib.sleep_timer import SleepTimer

service_locator = ServiceLocatorFactory.create()

service_state_store = service_locator.get(ServiceName.ServiceStateStore)
player = service_locator.get(ServiceName.Player)
sleep_timer = SleepTimer(service_state_store, player)

Logger.log("Starting sleep timer service")

# reset timer when starting the system to make sure we don't shut down immediately in some cases
sleep_timer.stop_timer()

while True:
    # Check every 15 seconds if we should shut down and delay for 10 seconds to give some room for emergency shutdown
    time.sleep(15)

    if sleep_timer.is_enabled():
        if player.is_playing():
            sleep_timer.stop_timer()
        else:
            sleep_timer.start_timer()

        if sleep_timer.is_running() and sleep_timer.is_sleep_timeout_reached():
            sleep_timer.sleep()
