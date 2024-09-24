#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/11/22
# Author: Red Shen <red@host.com.tw>
# You have to install aspell-en first.
import os, sys

USER_DATA = "/var/cpanel/userdata/"
FILE_EXTENSIONS = (".php")
ALLOW_LIST = []

def get_cmd_output(command):
    #print(command)
    return os.popen(command).read().strip()

def run_cmd(cmd, quiet = True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)
    
def check_suspicious(text):
    if text in ALLOW_LIST:
        return False
    if text.isdigit():
        return True
    if text.isalpha():
        spell_check = get_cmd_output("echo \"{0}\"|aspell --list".format(text))

        if spell_check == text:
            return True
            
    return False
    
def filename_has_ext(fn):
    ext = os.path.splitext(fn)[-1]

    if ext == "":
        return False
    else:
        return True

def filename_check():
    user = ""
    
    if len(sys.argv) >= 2:
        for x in (1, len(sys.argv) -1):
            if "-" not in sys.argv[x]:
                user = sys.argv[x]
                break
        
    search_path = "{0}{1}".format(USER_DATA, user)
    path_list = get_cmd_output("grep --exclude=*_SSL -hr documentroot: {0}".format(search_path))
    count = 0
    
    for line in path_list.splitlines():
        if "documentroot: " in line:
            target_dir = line.split()[1]
            input_path = os.path.join(target_dir, "wp-content/uploads/")
            #input_path = target_dir
            
            if not os.path.isdir(input_path):
                continue

            for dirname, dirnames, filenames in os.walk(input_path):
                for fn in filenames:
                    if fn.lower().endswith(FILE_EXTENSIONS) or not filename_has_ext(fn):
                        text = os.path.splitext(fn)[0]
                        
                        if not check_suspicious(text):
                            continue

                        full_path = os.path.join(dirname, fn)
                        count = count + 1

                        if verbose:
                            print(full_path)
                        if delete:
                            os.system("rm {0}".format(full_path))

    if verbose:
        print("Total: {0}".format(count))

if __name__ == "__main__":
    verbose = True
    delete = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-q" in sys.argv:
        verbose = False
    if "-f" in sys.argv:
        delete = True

    filename_check()

