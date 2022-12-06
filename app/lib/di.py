#!/usr/bin/env python

from enum import Enum

from lib.store import FakeStore, ServiceStateStore, SystemTagStore


class ServiceName(Enum):
    ServiceStateStore = "ServiceStateStore"
    SystemTagStore = "SystemTagStore"


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
            locator.register(ServiceName.SystemTagStore, FakeStore())
        else:
            locator.register(ServiceName.ServiceStateStore, ServiceStateStore())
            locator.register(ServiceName.SystemTagStore, SystemTagStore())

        return locator
