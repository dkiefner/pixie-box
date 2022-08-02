#!/usr/bin/env python
import subprocess

from common.logger import Logger


class Shell:
    @staticmethod
    def execute(cmd):
        Logger.log(f"Executing command: {cmd}")
        return subprocess.check_output(cmd, shell=True).decode()
