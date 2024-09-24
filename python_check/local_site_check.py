#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/10/19

import os
import sys
import time

SITE_LIST = "/etc/userdomains"


class Log:
    def __init__(self):
        self.log_path = "site_check_result.log"
        self.msgs = []
        log_file = open(self.log_path, "w")
        log_file.close()

    def add(self, msg):
        self.msgs.append(msg)
        print(msg)

    def write(self):
        log_file = open(self.log_path, "a")

        for msg in self.msgs:
            log_file.write("{0}\n".format(msg))

        log_file.close()
        self.msgs = []


def get_site_list():
    site_list_file = open(SITE_LIST, "r")
    site_list = site_list_file.read().splitlines()
    site_list_file.close()
    return site_list


def local_site_check():

    if not os.path.isfile(SITE_LIST):
        print("{0} not exist, abort.".format(SITE_LIST))
        return False

    site_list = get_site_list()

    for pair in site_list:
        site = pair.split(":")[0]
        now = time.localtime()
        date = time.strftime("%Y-%m%d-%H%M%S", now)
        log.add("{0}: {1}".format(date, site))
        cmd = "curl -k --connect-timeout 5 --max-time 10 -s http://{0} > /dev/null".format(
            site)
        os.system(cmd)
        cmd = "curl -k --connect-timeout 5 --max-time 10 -s https://{0} > /dev/null".format(
            site)
        os.system(cmd)

    log.write()


if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    log = Log()
    local_site_check()
