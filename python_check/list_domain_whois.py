#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/10/04

import os
import sys

USER_DATA = "/var/cpanel/userdata/"


def run_cmd(command, display=False):
    if display:
        print(command)

    return os.popen(command).read().strip()


def get_user_domains(input_path):
    domain_list = []
    main = open(input_path, "r")

    for line in main.readlines():
        if "sub_domains" in line:
            break
        if "main_domain: " in line:
            domain_list.append(line.replace("main_domain: ", "").strip())
        if "  - " in line:
            domain_list.append(line.replace("  - ", "").strip())

    main.close()
    return domain_list


def find_registar(domain):
    whois = run_cmd(
        "whois {0}|grep \"Registrar:\|Registration Service Provider:\"".format(domain))
    if whois != "":
        return whois.split(":")[1].strip()
    else:
        return whois


def list_domain_whois():
    domain_list = []

    for dirname, dirnames, filenames in os.walk(USER_DATA):
        for fn in filenames:
            if fn != "main":
                continue

            full_path = os.path.join(dirname, fn)
            domain_list = domain_list + get_user_domains(full_path)

    for domain in domain_list:
        print("{0}: {1}".format(domain, find_registar(domain)))


if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    list_domain_whois()
