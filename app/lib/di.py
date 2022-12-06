#!/usr/bin/env python

from enum import Enum

from lib.file_system import RealFileSystem
from lib.player import FakePlayer, LocalFilePlayer
from lib.rfid_reader import MFRC522Reader
from lib.shell import FakeShell, CommandShell
from lib.shutdown import FakeShutdown, SystemShutdown
from lib.sleep_timer import SleepTimer
from lib.store import FakeStore, ServiceStateStore, SystemTagStore
from lib.system_info import FakeSystemInfo, RealSystemInfo
from lib.volume import FakeVolume, AMixerVolume
from lib.zip import ZipArchiver


class ServiceName(Enum):
    FileArchiver = "FileArchiver"
    FileSystem = "FileSystem"
    Player = "Player"
    RFIDReader = "RFIDReader"
    ServiceStateStore = "ServiceStateStore"
    Shell = "Shell"
    Shutdown = "Shutdown"
    SleepTimer = "SleepTimer"
    SystemInfo = "SystemInfo"
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
            shell = FakeShell()
            locator.register(ServiceName.FileSystem, RealFileSystem(shell, "/Users/dannyk/src/pixiebox/"))
            locator.register(ServiceName.Player, FakePlayer())
            locator.register(ServiceName.ServiceStateStore, FakeStore())
            locator.register(ServiceName.Shell, shell)
            locator.register(ServiceName.Shutdown, FakeShutdown())
            locator.register(ServiceName.SystemInfo, FakeSystemInfo())
            locator.register(ServiceName.SystemTagStore, FakeStore())
            locator.register(ServiceName.Volume, FakeVolume())
        else:
            service_state_store = ServiceStateStore()
            shell = CommandShell()

            locator.register(ServiceName.FileSystem, RealFileSystem(shell, "/home/pi/pixiebox/"))
            locator.register(ServiceName.Player, LocalFilePlayer(service_state_store, shell))
            locator.register(ServiceName.ServiceStateStore, service_state_store)
            locator.register(ServiceName.Shell, shell)
            locator.register(ServiceName.Shutdown, SystemShutdown(shell))
            locator.register(ServiceName.SystemInfo, RealSystemInfo(shell))
            locator.register(ServiceName.SystemTagStore, SystemTagStore())
            locator.register(ServiceName.Volume, AMixerVolume(shell))

        locator.register(ServiceName.SleepTimer,
                         SleepTimer(
                             locator.get(ServiceName.ServiceStateStore),
                             locator.get(ServiceName.Player),
                             locator.get(ServiceName.Shutdown)
                         ))
        locator.register(ServiceName.RFIDReader, MFRC522Reader())
        locator.register(ServiceName.FileArchiver, ZipArchiver())

        return locator
