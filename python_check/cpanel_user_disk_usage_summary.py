#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/06/04

import os
import sys
import json

USER_LOCATION = "/var/cpanel/users"


def get_cmd_output(command):
    # print(command)
    return os.popen(command).read().strip()


def run_cmd(cmd, quiet=True, logging=False):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"
    if logging == True:
        log.write(cmd)

    os.system(cmd)


def cpanel_user_disk_usage_summary():
    total_usage = 0
    print("Calculating....")

    for user in os.listdir(USER_LOCATION):
        raw_data = get_cmd_output(
            "whmapi1 accountsummary user={0} --output=json".format(user))
        json_data = json.loads(raw_data)

        if json_data["metadata"]["result"] == 1:
            disk_usage_raw = json_data["data"]["acct"][0]["diskused"]
            disk_usage = int(disk_usage_raw .strip("M"))
            total_usage = total_usage + disk_usage

            if verbose:
                print(disk_usage_raw)

    print("")
    print("Total:")
    print("{0} GB".format(total_usage / 1024))


if __name__ == "__main__":
    verbose = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    if "-v" in sys.argv:
        verbose = True

    cpanel_user_disk_usage_summary()
