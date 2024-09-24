#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2018/12/19
# Author: Red Shen <red@noc.tw>
import os, sys

from subprocess import PIPE, Popen

USER_DATA = "/var/cpanel/userdata/"

def get_command_output(command):
    proc = Popen(command.split(), stdout=PIPE)
    return proc.communicate()[0].strip()

def run_cmd(cmd, quiet = True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)

def user_set_nobody():
    do_change = False

    if len(sys.argv) >= 2:
        account = sys.argv[1]
        user_data_path = os.path.join(USER_DATA, account)
        path_list = get_command_output("grep -hr documentroot: {0}".format(user_data_path))
        
        if len(sys.argv) >= 3 and sys.argv[2] == "set":
            do_change = True
        
        for line in path_list.splitlines():
            if "documentroot: " in line:
                target_dir = line.split()[1]
                
                if do_change == True:
                    cmd = "chown {0}:nobody {1}".format(account, target_dir)
                    run_cmd(cmd)
                    
                cmd = "stat -c \"%U:%G %n\" {0}".format(target_dir)
                run_cmd(cmd, quiet = False)
        
if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    user_set_nobody()

