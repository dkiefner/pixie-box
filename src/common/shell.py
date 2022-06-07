#!/usr/bin/env python
import os


class Shell:
    @staticmethod
    def execute(cmd):
        os.system(cmd)
