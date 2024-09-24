#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/07/12

import os
import sys

HTACCESS_BODY = '''AuthType Basic
AuthName "Abuse - TWNOC <TICKET-ID>"
AuthUserFile "/home/<USER>/.htpasswds/public_html/passwd"
require valid-user
'''


def get_cmd_output(command):
    # print(command)
    return os.popen(command).read().strip()


def run_cmd(cmd, quiet=True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)


def fast_htaccess_forbid():
    if len(sys.argv) >= 2:
        username = sys.argv[1]
    else:
        return False

    if os.path.isdir("/home/{0}".format(username)):
        # htaccess_path = "/home/{0}/public_html/.htaccess".format(username)
        htaccess_path = "/home/{0}/.htaccess".format(username)
        passwd_path = "/home/{0}/.htpasswds/public_html/passwd".format(
            username)
        body = ""
        os.system("mkdir -p /home/{0}/.htpasswds/public_html".format(username))
        passwd = open(passwd_path, "w")
        passwd.write("user:$apr1$cSQmQAFL$fHIWoZ69uFTm/U652jHuQ/")
        passwd.close()

        if os.path.isfile(htaccess_path):
            htaccess = open(htaccess_path, "r")
            body = body + htaccess.read()
            htaccess.close()

        insertion = HTACCESS_BODY.replace("<USER>", username)

        if len(sys.argv) >= 3:
            insertion = insertion.replace("<TICKET-ID>", sys.argv[2])

        htaccess = open(htaccess_path, "w")
        htaccess.write(insertion)
        htaccess.write(body)
        htaccess.close()
    else:
        print("Username incorrect, abort.")


if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    fast_htaccess_forbid()
