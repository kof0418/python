#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018/12/06

import os
import sys

from subprocess import PIPE, Popen


def get_command_output(command):
    proc = Popen(command.split(), stdout=PIPE)
    return proc.communicate()[0].strip()


def get_memory_total():
    meminfo = get_command_output("cat /proc/meminfo")

    for line in meminfo.split("\n"):
        if "MemTotal:" in line:
            mem_total = int(line.split()[1])
            break

    return mem_total / 1024


def user_memory_limits_summary():
    total_amount = 0
    result = get_command_output("lvectl limits all")

    for line in result.splitlines()[3:]:
        items = line.split()
        user = items[0]
        limit = items[2]

        if user != "limit" and limit != "0K":
            converted_limit = int(limit.rstrip("MB"))
            if converted_limit != 0:
                total_amount = total_amount + converted_limit
                if verbose:
                    print("{0} - {1} MB".format(user, converted_limit))

    if verbose:
        print("")
        print("Total:")

    memory_total = get_memory_total()

    if memory_total < 1024:
        unit = "MB"
    else:
        memory_total = memory_total / 1024
        total_amount = total_amount / 1024
        unit = "GB"

    print("{0}% - {1} {2} / {3} {4} ".format(int(total_amount * 100 /
          memory_total), total_amount,  unit, memory_total, unit))


if __name__ == "__main__":
    verbose = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-v" in sys.argv:
        verbose = True

    user_memory_limits_summary()
