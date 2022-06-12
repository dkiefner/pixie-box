#!/usr/bin/env python
import os

from app.common.logger import Logger


class Shell:
    @staticmethod
    def execute(cmd):
        Logger.log(f"Executing command: {cmd}")
        os.system(cmd)
