#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/11/10

import os
import sys

RECIPIENT = "abuse@twnoc.net"
CXS_COMMAND = "/usr/sbin/cxs --background --nobayes --virusscan --filemax 100000 --smtp --exploitscan --nofallback --html --ignore /etc/cxs/cxs.ignore --logfile /var/log/cxs.log --options mMOLfSGchdnZRD --throttle 20 --quiet --report /var/log/cxs.scan --sizemax 500000 --ssl --summary --sversionscan --template /etc/cxs/cxs.template"


def easy_cxs_scan():
    user = ""

    if len(sys.argv) >= 2:
        for x in (1, len(sys.argv) - 1):
            if "-" not in sys.argv[x]:
                user = sys.argv[x]
                break

    if user == "":
        return False

    os.system("rm -f /home/{0}/.contactemail".format(user))
    os.system("{0} --mail {1} --user {2}".format(CXS_COMMAND, RECIPIENT, user))
    os.system("ps aux|grep cxs|grep -v grep")
    os.system("du -sh /home/{0}".format(user))


if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    easy_cxs_scan()
