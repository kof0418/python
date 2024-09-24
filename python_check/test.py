#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/12/25

import os
import sys
import shlex

DEFAULT_WARNING_PERCENTAGE = 90
DEFAULT_CRITICAL_PERCENTAGE = 95
DEFAULT_WARNING_FREE = 1
DEFAULT_CRITICAL_FREE = 0.8


def get_cmd_output(command):
    # print(command)
    return os.popen(command).read().strip()


def check_memory():
    warning_percentage = DEFAULT_WARNING_PERCENTAGE
    critical_percentage = DEFAULT_CRITICAL_PERCENTAGE
    warning_free = DEFAULT_WARNING_FREE
    critical_free = DEFAULT_CRITICAL_FREE

    if len(sys.argv) >= 2 and sys.argv[1].replace(".", "", 1).isdigit():
        warning_percentage = float(sys.argv[1])
    if len(sys.argv) >= 3 and sys.argv[2].replace(".", "", 1).isdigit():
        critical_percentage = float(sys.argv[2])
    if len(sys.argv) >= 4 and sys.argv[3].replace(".", "", 1).isdigit():
        warning_free = float(sys.argv[3])
    if len(sys.argv) >= 5 and sys.argv[4].replace(".", "", 1).isdigit():
        critical_free = float(sys.argv[4])

    if "--debug" in sys.argv:
        print("Warning percentage = {0}".format(warning_percentage))
        print("Critical percentage = {0}".format(critical_percentage))
        print("Warning free memory = *{0}".format(warning_free))
        print("Critical free memory = *{0}".format(critical_free))

    meminfo = get_cmd_output("cat /proc/meminfo")
    min_free_kbytes = int(get_cmd_output("cat /proc/sys/vm/min_free_kbytes"))
    matches = 0

    for line in meminfo.splitlines():
        items = shlex.split(line)

        if items[0] == "MemTotal:":
            mem_total = int(items[1])
            matches = matches + 1
        elif items[0] == "MemFree:":
            mem_free = int(items[1])
            matches = matches + 1
        elif items[0] == "Buffers:":
            buffers = int(items[1])
            matches = matches + 1
        elif items[0] == "Cached:":
            cached = int(items[1])
            matches = matches + 1
        elif items[0] == "Slab:":
            slab = int(items[1])
            matches = matches + 1

        if matches == 5:
            break

    if "MemAvailable:" in meminfo:
        mem_available = mem_free + buffers + cached + slab
    else:
        mem_available = mem_free + buffers + cached

    used_mem = mem_total - mem_available
    percentage = int(used_mem * 100 / mem_total)

    if mem_total < 1048576:
        msg = "{0}% - {1} / {2} MB used. Free memory: {3} MB, min free memory: {4} MB.".format(percentage, int(
            used_mem / 1024), int(mem_total / 1024), int(mem_free / 1024), int(min_free_kbytes / 1024))
    else:
        msg = "{0}% - {1} / {2} GB used. Free memory: {3} MB, min free memory: {4} MB.".format(percentage, int(
            used_mem / 1024 / 1024), int(mem_total / 1024 / 1024), int(mem_free / 1024), int(min_free_kbytes / 1024))

    print(msg)

    if percentage >= critical_percentage or mem_free <= (min_free_kbytes * critical_free):
        sys.exit(2)
    elif percentage >= warning_percentage or mem_free <= (min_free_kbytes * warning_free):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    check_memory()
