#!/usr/bin/env python

from datetime import datetime


class Logger:
    @staticmethod
    def log(value):
        print(f"{datetime.now()}: {value}")
