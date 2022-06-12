#!/usr/bin/env python
import os

from pixiebox.common.logger import Logger


class Shell:
    @staticmethod
    def execute(cmd):
        Logger.log(f"Executing command: {cmd}")
        os.system(cmd)
