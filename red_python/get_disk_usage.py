#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/05/05
# Author: Red Shen <red@host.com.tw>
import os, sys
import shlex

def get_cmd_output(command):
    #print(command)
    return os.popen(command).read().strip()

def run_cmd(cmd, quiet = True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)

def get_disk_usage():
    df = get_cmd_output("df -ah")
    
    for line in df.splitlines():
        items = shlex.split(line)
        
        if "Filesystem" in line:
            print(line)
        if items[5] == "/" and items[0] != "rootfs":
            print(line)
            break

if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    get_disk_usage()

