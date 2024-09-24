#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018/11/11

import os
import sys

from subprocess import PIPE, Popen


def get_command_output(command):
    proc = Popen(command.split(), stdout=PIPE)
    return proc.communicate()[0].strip()


def user_quota_summary():
    total_amount = 0
    result = get_command_output("repquota -a")

    for line in result.splitlines()[5:]:
        items = line.split()
        user = items[0]
        limit = items[4]

        if limit.isdigit():
            converted_limit = int(limit)
            if converted_limit != 0:
                total_amount = total_amount + converted_limit
                if verbose:
                    print("{0} - {1} GB".format(user,
                          converted_limit / 1024 / 1024))

    if verbose:
        print("")

    print("Total:")
    print("{0} GB".format(total_amount / 1024 / 1024))
    print("{0} TB".format(total_amount / 1024 / 1024 / 1024))


if __name__ == "__main__":
    verbose = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-v" in sys.argv:
        verbose = True

    user_quota_summary()
