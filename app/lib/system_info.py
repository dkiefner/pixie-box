#!/usr/bin/env python

from lib.shell import Shell


class SystemInfo:
    LOG_MAX_LINES = 500

    @staticmethod
    def gpu_temp():
        return Shell.execute("vcgencmd measure_temp | cut -d\"=\" -f 2 | cut -d\"'\" -f 1")

    @staticmethod
    def cpu_temp():
        return Shell.execute("cpu=$(</sys/class/thermal/thermal_zone0/temp);echo $((cpu/1000))")

    @staticmethod
    def pixiebox_logs():
        return SystemInfo.__get_journal_for_service("pixiebox")

    @staticmethod
    def web_app_logs():
        return SystemInfo.__get_journal_for_service("pixiebox_webapp")

    @staticmethod
    def sleep_timer_logs():
        return SystemInfo.__get_journal_for_service("sleep_timer")

    @staticmethod
    def __get_journal_for_service(service_name):
        return Shell.execute(
            f"sudo journalctl --unit={service_name} -r -n {SystemInfo.LOG_MAX_LINES} --no-pager").split('\n')
