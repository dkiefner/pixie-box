#!/usr/bin/env python

from lib.shell import Shell


class SystemInfo:

    @staticmethod
    def gpu_temp():
        Shell.execute("vcgencmd measure_temp | cut -d\"=\" -f 2 | cut -d\"'\" -f 1")

    @staticmethod
    def cpu_temp():
        Shell.execute("cpu=$(</sys/class/thermal/thermal_zone0/temp);echo \"$((cpu/1000))\"")
