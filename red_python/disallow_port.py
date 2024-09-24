#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/07/16
# Author: Red Shen <red@host.com.tw>
import os, sys, re

DISALLOW_PORTS = ["25", "465", "587"]
CSF_CONFIG = "/etc/csf/csf.conf"

def get_cmd_output(command):
    #print(command)
    return os.popen(command).read().strip()
    
def run_cmd(cmd, silence = True):
    if silence == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)
    
def get_port_list():
    config = open(CSF_CONFIG, "r")
    content = config.read()
    config.close()
    pattern = re.compile("TCP_OUT = \"(.*?)\"")
    result = pattern.findall(content)

    if len(result) >= 1:
        return result[0].split(",")
    else:
        return []

def set_port_list(port_list):
    new_set = ",".join(port_list)
    config = open(CSF_CONFIG, "r")
    content = config.read()
    config.close()
    pattern = re.compile("TCP_OUT = \"(.*?)\"")
    result = pattern.findall(content)

    if len(result) >= 1:
        old_set = result[0]
        content = content.replace(old_set, new_set)
        run_cmd("/bin/cp -f {0} {0}.bak".format(CSF_CONFIG, CSF_CONFIG))
        config = open(CSF_CONFIG, "w")
        config.write(content)
        config.close()

def disallow_port():
    port_list = get_port_list()
    restart_required = False

    for port in DISALLOW_PORTS:
        if port in port_list:
            port_list.remove(port)
            print("Port '{0}' removed.".format(port))

            if restart_required != True:
                restart_required = True

    if restart_required == True:
        print("Writing to {0}".format(CSF_CONFIG))
        set_port_list(port_list)
        print("Restarting CSF....")
        os.system("/usr/sbin/csf -r")
        
    print("Completed.")

if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    disallow_port()

