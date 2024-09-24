#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/11/19

import os
import sys
import shlex

OPTION_LIST = ["client", "client-detailed", "protocol", "vhost", "request"]


def run_cmd(command, display=False):
    if display:
        print(command)

    return os.popen(command).read().strip()


def get_ip_country(ip):
    if ":" in ip:
        geoip = run_cmd("/usr/bin/geoiplookup6 {0}".format(ip))
    else:
        geoip = run_cmd("/usr/bin/geoiplookup {0}".format(ip))

    return geoip.splitlines()[0].replace("GeoIP Country Edition:", "").replace("GeoIP Country V6 Edition:", "").strip()


def get_ip_domain(ip):
    return run_cmd("/usr/bin/dig +short -x {0}".format(ip))


def apache_sort():
    if len(sys.argv) < 2 or sys.argv[1] not in OPTION_LIST:
        print("Usage: {0} <{1}> <(optional) keyword>".format(
            sys.argv[0], ", ".join(OPTION_LIST)))
        return False

    if len(sys.argv) >= 3:
        status = run_cmd(
            "/usr/sbin/apachectl fullstatus|grep {0}".format(sys.argv[2]))
    else:
        status = run_cmd("/usr/sbin/apachectl fullstatus")

    data_list = []

    for line in status.splitlines():
        if "h2" in line or "http/1.1" in line:
            items = shlex.split(line, posix=False)

            if len(items) >= 16:
                if sys.argv[1] == "request":
                    data_list.append(items[15])
            if len(items) >= 14:
                if sys.argv[1] == "client":
                    data_list.append(items[11])
                elif sys.argv[1] == "client-detailed":
                    data_list.append(items[11])
                elif sys.argv[1] == "protocol":
                    data_list.append(items[12])
                elif sys.argv[1] == "vhost":
                    data_list.append(items[13])

    for count, elem in sorted(((data_list.count(i), i) for i in set(data_list))):
        if sys.argv[1] == "client-detailed":
            print("{0}: {1} ({2} {3})".format(elem, count,
                  get_ip_country(elem), get_ip_domain(elem)))
        else:
            print("{0}: {1}".format(elem, count))


if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    apache_sort()
