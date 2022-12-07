#!/usr/bin/env python
import subprocess

from lib.logger import Logger


class Shell:
    def execute(self, cmd):
        pass


class CommandShell(Shell):
    def execute(self, cmd):
        Logger.log(f"Executing command: {cmd}")
        return subprocess.check_output(cmd, shell=True).decode()


class FakeShell(Shell):
    def execute(self, cmd):
        Logger.log(f"Executing command: {cmd}")
