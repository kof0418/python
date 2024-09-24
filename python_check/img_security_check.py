#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/11/15

import os
import sys
import time

USER_DATA = "/var/cpanel/userdata/"
# FILE_EXTENSIONS = (".jpg", ".png", ".ico")
FILE_EXTENSIONS = (".ico")
ALLOWED_KEYWORD = ["image", "icon"]


def get_cmd_output(command):
    # print(command)
    return os.popen(command).read().strip()


def run_cmd(cmd, quiet=True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)


def get_date():
    now = time.localtime()
    date = time.strftime("%Y-%m%d-%H:%M:%S", now)
    return date


def img_infected(path):
    # print(path)
    file_type = get_cmd_output("file \"{0}\"".format(path))

    if file_type == "":
        print("Failed to open: {0}".format(path))

    if ":" in file_type:
        description = file_type.split(":")[1]

        if "text" in description:
            return True
        if not any(keyword in description for keyword in ALLOWED_KEYWORD):
            return True

    return False


def img_security_check(input_path):
    infected = False

    for dirname, dirnames, filenames in os.walk(input_path):
        for fn in filenames:
            if fn.lower().endswith(FILE_EXTENSIONS):
                full_path = os.path.join(dirname, fn)

                if img_infected(full_path):
                    if infected != True:
                        infected = True
                    if verbose:
                        print(full_path)
                    if delete:
                        os.system("rm {0}".format(full_path))

    if infected:
        return True
    else:
        return False


def fetch_list():
    input_list = []

    if len(sys.argv) >= 2:
        for x in (1, len(sys.argv) - 1):
            if "-" not in sys.argv[x]:
                input_list.append(os.path.join("/home/", sys.argv[1]))
                return input_list
    else:
        for dir in os.listdir(USER_DATA):
            input_list.append(os.path.expanduser(os.path.join("/home/", dir)))

    return input_list


def main_loop():
    total_count = 0
    infected_count = 0
    input_list = fetch_list()

    if verbose:
        print("Scanning.... {0}".format(get_date()))

    for input_path in input_list:
        if os.path.isdir(input_path):
            # print(input_path)
            total_count = total_count + 1

            if img_security_check(input_path):
                infected_count = infected_count + 1

    if verbose:
        percentage = int(infected_count * 100 / total_count)
        print("Finishing.... {0}".format(get_date()))
        print("Total: {0}% - {1} / {2} accounts infected.".format(percentage,
              infected_count, total_count))


if __name__ == "__main__":
    verbose = True
    delete = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-q" in sys.argv:
        verbose = False
    if "-f" in sys.argv:
        delete = True

    main_loop()
