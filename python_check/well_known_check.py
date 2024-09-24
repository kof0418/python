#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/09/13

import os
import sys

USER_DATA = "/var/cpanel/userdata/"
FILE_EXTENSIONS = (".php", ".ico", ".suspected")


def get_cmd_output(command):
    # print(command)
    return os.popen(command).read().strip()


def run_cmd(cmd, quiet=True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)


def well_known_check():
    user = ""

    if len(sys.argv) >= 2:
        for x in (1, len(sys.argv) - 1):
            if "-" not in sys.argv[x]:
                user = sys.argv[x]
                break

    search_path = "{0}{1}".format(USER_DATA, user)
    path_list = get_cmd_output(
        "grep --exclude=*_SSL -hr documentroot: {0}".format(search_path))
    count = 0

    for line in path_list.splitlines():
        if "documentroot: " in line:
            target_dir = line.split()[1]
            input_path = os.path.join(target_dir, ".well-known")

            for dirname, dirnames, filenames in os.walk(input_path):
                for fn in filenames:
                    if fn.lower().endswith(FILE_EXTENSIONS):
                        count = count + 1
                        full_path = os.path.join(dirname, fn)

                        if verbose:
                            print(full_path)
                        if delete:
                            os.system("rm {0}".format(full_path))

    if verbose:
        print("Total: {0}".format(count))


if __name__ == "__main__":
    verbose = True
    delete = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-q" in sys.argv:
        verbose = False
    if "-f" in sys.argv:
        delete = True

    well_known_check()
