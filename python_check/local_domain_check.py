#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/10/19

import os
import sys

DOMAIN_LIST = "/etc/userdomains"
OLD_IP_LIST = "old_ip.txt"
NEW_IP_LIST = "new_ip.txt"


def get_list(input_path):
    data_list = []

    if os.path.isfile(input_path):
        input_file = open(input_path, "r")
        for line in input_file.readlines():
            if "#" not in line and line.strip() != "":
                data_list.append(line.strip())

    return data_list


def run_cmd(command, display=False):
    if display:
        print(command)

    return os.popen(command).read().strip()


def local_domain_check():
    domain_list = get_list(DOMAIN_LIST)
    old_ip = get_list(OLD_IP_LIST)
    new_ip = get_list(NEW_IP_LIST)
    old_set = 0
    new_set = 0
    detail_set = []

    for pair in domain_list:
        domain = pair.split(":")[0]
        cmd = "dig +short {0}".format(domain)
        result = run_cmd(cmd)

        if verbose:
            print("{0}: {1}".format(domain, result))

        if result in old_ip:
            old_set = old_set + 1
            detail_set.append("{0}: {1}".format(domain, result))
        elif result in new_ip:
            new_set = new_set + 1

    if not verbose:
        for detail in detail_set:
            print(detail)

    print("\nSummary:")
    print("Domains total: {0}".format(len(domain_list)))
    print("Old IP: {0}".format(old_set))
    print("New IP: {0}".format(new_set))


if __name__ == "__main__":
    verbose = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-v" in sys.argv:
        verbose = True

    local_domain_check()
