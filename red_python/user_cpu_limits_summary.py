#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018/12/18
# Author: Red Shen <red@noc.tw>
import os, sys

from subprocess import PIPE, Popen

def get_command_output(command):
    proc = Popen(command.split(), stdout=PIPE)
    return proc.communicate()[0].strip()

def user_cpu_limits_summary():
    cpu_total = int(get_command_output("grep -c ^processor /proc/cpuinfo")) * 100
    result = get_command_output("lvectl limits all")
    user_total = 0
    
    for line in result.splitlines()[3:]:
        items = line.split()
        user = items[0]
        speed = items[1]
        
        if user != "limit" and user != "3":
            converted_speed = int(speed)
            user_total = user_total + converted_speed
            
            if verbose:
                print("{0} - {1}".format(user, converted_speed))

    if verbose:
        print("")
        print("Total:")

    print("{0}% - {1} / {2}".format(int(user_total * 100 / cpu_total), user_total,  cpu_total))
            
if __name__ == "__main__":
    verbose = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    
    if "-v" in sys.argv:
        verbose = True
    
    user_cpu_limits_summary()

