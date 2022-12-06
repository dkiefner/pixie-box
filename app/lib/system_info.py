#!/usr/bin/env python


class SystemInfo:
    def gpu_temp(self):
        pass

    def cpu_temp(self):
        pass

    def pixiebox_logs(self):
        pass

    def web_app_logs(self):
        pass

    def sleep_timer_logs(self):
        pass


class RealSystemInfo(SystemInfo):
    __LOG_MAX_LINES = 500

    def __init__(self, shell):
        self.shell = shell

    def gpu_temp(self):
        return self.shell.execute("vcgencmd measure_temp | cut -d\"=\" -f 2 | cut -d\"'\" -f 1")

    def cpu_temp(self):
        temp_by_1000 = self.shell.execute("cat /sys/class/thermal/thermal_zone0/temp")
        return str(int(temp_by_1000) // 1000)

    def pixiebox_logs(self):
        return self.__get_journal_for_service("pixiebox")

    def web_app_logs(self):
        return self.__get_journal_for_service("pixiebox_webapp")

    def sleep_timer_logs(self):
        return self.__get_journal_for_service("sleep_timer")

    def __get_journal_for_service(self, service_name):
        return self.shell.execute(
            f"sudo journalctl --unit={service_name} -r -n {self.__LOG_MAX_LINES} --no-pager").split('\n')


class FakeSystemInfo(SystemInfo):
    def gpu_temp(self):
        return "-1"

    def cpu_temp(self):
        return "-1"

    def pixiebox_logs(self):
        return """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                """

    def web_app_logs(self):
        return """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                """

    def sleep_timer_logs(self):
        return """
                Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                """
