#!/usr/bin/env python

import dbm

from common.logger import Logger


class SystemTagStore:
    __store_name = "system-tag-store"

    def save(self, key, value):
        Logger.log(f"Storing {key}={value}")
        with dbm.open(self.__store_name, 'c') as store:
            store[str(key)] = value
            store.close()

    def get(self, key):
        with dbm.open(self.__store_name, 'c') as store:
            value = store.get(str(key))
            store.close()
            return value
