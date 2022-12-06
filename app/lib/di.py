#!/usr/bin/env python

from enum import Enum

from lib.player import FakePlayer, LocalFilePlayer
from lib.shutdown import FakeShutdown, SystemShutdown
from lib.sleep_timer import SleepTimer
from lib.store import FakeStore, ServiceStateStore, SystemTagStore
from lib.volume import FakeVolume, AMixerVolume


class ServiceName(Enum):
    Player = "Player"
    ServiceStateStore = "ServiceStateStore"
    Shutdown = "Shutdown"
    SleepTimer = "SleepTimer"
    SystemTagStore = "SystemTagStore"
    Volume = "Volume"


class ServiceLocator:
    __services = {}

    def register(self, name, service):
        self.__services[name] = service

    def get(self, name):
        return self.__services[name]


class ServiceLocatorFactory:

    @staticmethod
    def create(is_development=False):
        locator = ServiceLocator()

        if is_development:
            locator.register(ServiceName.ServiceStateStore, FakeStore())
            locator.register(ServiceName.Shutdown, FakeShutdown())
            locator.register(ServiceName.SystemTagStore, FakeStore())
            locator.register(ServiceName.Player, FakePlayer())
            locator.register(ServiceName.Volume, FakeVolume())
        else:
            service_state_store = ServiceStateStore()
            locator.register(ServiceName.ServiceStateStore, service_state_store)
            locator.register(ServiceName.Shutdown, SystemShutdown())
            locator.register(ServiceName.SystemTagStore, SystemTagStore())
            locator.register(ServiceName.Player, LocalFilePlayer(service_state_store))
            locator.register(ServiceName.Volume, AMixerVolume())

        locator.register(ServiceName.SleepTimer,
                         SleepTimer(
                             locator.get(ServiceName.ServiceStateStore),
                             locator.get(ServiceName.Player),
                             locator.get(ServiceName.Shutdown)
                         ))

        return locator
