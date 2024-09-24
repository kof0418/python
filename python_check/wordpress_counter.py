#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/03/26

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


def wordpress_counter():
    path_list = get_cmd_output(
        "grep --exclude=*_SSL -hr documentroot: {0}".format(USER_DATA))
    site_count = 0
    wp_count = 0

    for line in path_list.splitlines():
        if "documentroot: " in line:
            site_count = site_count + 1
            target_dir = line.split()[1]
            wp_config = os.path.join(target_dir, "wp-config.php")

            if os.path.isfile(wp_config):
                wp_count = wp_count + 1

                if verbose:
                    print(wp_config)

    print("Total: {0}% - {1} / {2}".format(wp_count *
          100 / site_count, wp_count, site_count))


if __name__ == "__main__":
    verbose = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-v" in sys.argv:
        verbose = True

    wordpress_counter()
