#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/08/09

import os
import sys

USER_DATA = "/var/cpanel/userdata/"


def get_cmd_output(command):
    # print(command)
    return os.popen(command).read().strip()


def run_cmd(cmd, quiet=True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)


def default_email_cleanup(input_path):
    if "/mail/new/" not in input_path and "/mail/cur/" not in input_path:
        return False

    count = 0

    for dirname, dirnames, filenames in os.walk(input_path):
        for fn in filenames:
            full_path = os.path.join(dirname, fn)
            count = count + 1
            # print(full_path)
            if delete:
                os.system("rm {0}".format(full_path))

    print("{0}: {1}".format(input_path, count))


def fetch_list():
    input_list = []

    if len(sys.argv) >= 2:
        for x in (1, len(sys.argv) - 1):
            if "-" not in sys.argv[x]:
                input_list.append(os.path.join(
                    "/home/", sys.argv[x], "mail", "new/"))
                input_list.append(os.path.join(
                    "/home/", sys.argv[x], "mail", "cur/"))
                return input_list
    else:
        for dir in os.listdir(USER_DATA):
            input_list.append(os.path.join("/home/", dir, "mail", "new/"))
            input_list.append(os.path.join("/home/", dir, "mail", "cur/"))

    return input_list


def main_loop():
    input_list = fetch_list()

    for input_path in input_list:
        if os.path.isdir(input_path):
            default_email_cleanup(os.path.join(input_path))


if __name__ == "__main__":
    delete = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-f" in sys.argv:
        delete = True

    main_loop()
