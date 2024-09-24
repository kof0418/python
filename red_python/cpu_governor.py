#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018/12/21
# Author: Red Shen <red@noc.tw>
import os, sys

from subprocess import PIPE, Popen

GOVERNOR_COMMAND = "echo <MODE> | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
FREQ_COMMAND = "echo <FREQ> | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq"

def get_command_output(command):
    proc = Popen(command.split(), stdout=PIPE)
    return proc.communicate()[0].strip()

def run_cmd(cmd, quiet = True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)

def cpu_governor():
    mode = ""
    freq = get_command_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq")
    
    if len(sys.argv) >= 2:
        if sys.argv[1] == "on":
            mode = "performance"
            freq = get_command_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
            
        elif sys.argv[1] == "off":
            mode = "powersave"
    
        if mode != "":
            cmd = GOVERNOR_COMMAND.replace("<MODE>", mode)
            run_cmd(cmd)
            #cmd = FREQ_COMMAND.replace("<FREQ>", freq)
            #run_cmd(cmd)
        
if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    cpu_governor()

