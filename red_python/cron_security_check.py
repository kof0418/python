#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/10/26
# Author: Red Shen <red@host.com.tw>
import os, sys
import cgi
import smtplib
import socket

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_NOTIFICATION = True
RECIPIENT = "abuse@twnoc.net"
CRON_PATH = "/var/spool/cron/"
CXS_COMMAND = "/usr/sbin/cxs --background --nobayes --virusscan --filemax 100000 --smtp --exploitscan --nofallback --html --ignore /etc/cxs/cxs.ignore --logfile /var/log/cxs.log --options mMOLfSGchdnZRD --throttle 20 --quiet --report /var/log/cxs.scan --sizemax 500000 --ssl --summary --sversionscan --template /etc/cxs/cxs.template"

def get_cmd_output(command):
    #print(command)
    return os.popen(command).read().strip()

def run_cmd(cmd, quiet = True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)

def send_mail(subject, body):
    if EMAIL_NOTIFICATION == False:
        return False

    hostname = socket.gethostname()
    sender = "root@{0}".format(hostname)
    recipient = RECIPIENT
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    html = MIMEText(cgi.escape(body).replace("\n", "<br>\n"), "html")
    msg.attach(html)
    
    try:
        mail = smtplib.SMTP("localhost")
        mail.sendmail(sender, recipient, msg.as_string())
        mail.quit()
        #print(msg.as_string())
    except:
        pass

def cron_security_check():
    cron_list = get_cmd_output("grep -Flr /var/tmp/ {0}".format(CRON_PATH))
    msgs = []

    for line in cron_list.splitlines():
        content = get_cmd_output("cat {0}".format(line))
        msgs.append(line)
        msgs.append(content)

        if verbose:
            print(line)
            print(content)

        if do_scan:
            username = line.replace(CRON_PATH, "").strip()
            os.system("rm -f /home/{0}/.contactemail".format(username))
            os.system("{0} --mail {1} --user {2}".format(CXS_COMMAND, RECIPIENT, username))

    if cron_list != "" and do_scan:
        send_mail("Suspicious User Cron Jobs", "CXS has been executed automatically, please wait for the reports.\n\n{0}".format("\n".join(msgs)))

if __name__ == "__main__":
    verbose = True
    do_scan = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-q" in sys.argv:
        verbose = False
    if "-c" in sys.argv:
        do_scan = True

    cron_security_check()

