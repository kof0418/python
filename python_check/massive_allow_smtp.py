#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/05/04

import os
import sys
import re

DOMAIN_LIST = "list.txt"
CSF_CONFIG = "/etc/csf/csf.conf"


def get_list(input_path):
    data_list = []

    if not os.path.isfile(input_path):
        return data_list

    input_file = open(input_path, "r")

    for line in input_file.readlines():
        if "#" not in line and line.strip() != "":
            data_list.append(line.strip())

    return data_list


def get_cmd_output(command):
    # print(command)
    return os.popen(command).read().strip()


def run_cmd(cmd, silence=True):
    if silence == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)


def get_smtp_user_list():
    config = open(CSF_CONFIG, "r")
    content = config.read()
    config.close()
    pattern = re.compile("SMTP_ALLOWUSER = \"(.*?)\"")
    result = pattern.findall(content)

    if len(result) >= 1:
        return result[0].split(",")
    else:
        return []


def set_smtp_user_list(smtp_user_list):
    new_set = ",".join(smtp_user_list)
    config = open(CSF_CONFIG, "r")
    content = config.read()
    config.close()
    pattern = re.compile("SMTP_ALLOWUSER = \"(.*?)\"")
    result = pattern.findall(content)

    if len(result) >= 1:
        old_set = result[0]
        content = content.replace(old_set, new_set)
        run_cmd("/bin/cp -f {0} {0}.bak".format(CSF_CONFIG, CSF_CONFIG))
        config = open(CSF_CONFIG, "w")
        config.write(content)
        config.close()


def massive_allow_smtp():
    domain_list = get_list(DOMAIN_LIST)
    smtp_user_list = get_smtp_user_list()
    user_list = []
    restart_required = False
    print("Domain searching....")

    for domain in domain_list:
        user = get_cmd_output("/scripts/whoowns {0}".format(domain))
        if user != "":
            user_list.append(user)

    print("User searching....")

    for user in user_list:
        if user not in smtp_user_list:
            smtp_user_list.append(user)
            print("User '{0}' added.".format(user))

            if restart_required != True:
                restart_required = True
        else:
            print("User '{0}' already in the list.".format(user))

    if restart_required == True:
        print("Writing to {0}".format(CSF_CONFIG))
        set_smtp_user_list(smtp_user_list)
        print("Restarting CSF....")
        os.system("/usr/sbin/csf -r")

    print("Completed.")


if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    massive_allow_smtp()
