#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2019/12/17
# Author: Red Shen <red@host.com.tw>
# 2024/01/24
# Modified by Adwin Xie
import os
import re
import smtplib
import socket
import sys
import time
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.version_info >= (3, 4):
    from html import escape
else:
    from cgi import escape

RESELLER = False
EMAIL_NOTIFICATION = True
RECIPIENT = "abuse@twnoc.net"
RESERVED_LIST = ["root", "mailnull", "cpanel"]
DELIVERY_LIMIT = 100
MAX_DELIVERY_LIMIT = 300


def run_cmd(command: str, display: bool = False) -> str:
    if display:
        print(command)

    result = subprocess.run(command, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()


def send_mail(subject: str, body: str) -> None:
    if EMAIL_NOTIFICATION is False:
        return False

    hostname = socket.gethostname()
    sender = "root@{0}".format(hostname)
    recipient = RECIPIENT
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    html = MIMEText(escape(body).replace("\n", "<br>\n"), "html")
    msg.attach(html)

    try:
        mail = smtplib.SMTP("localhost")
        mail.sendmail(sender, recipient, msg.as_string())
        mail.quit()
        # print(msg.as_string())
    except:
        pass


def find_user(text: str) -> str:
    if "B=identify_local_connection" in text:
        return re.findall(r" S=(.*?) ", text)[0]

    if "P=local" in text:
        return re.findall(r" U=(.*?) ", text)[0]

    return ""


def drop_user(user: str, count: int, max_mail_per_hour: int) -> None:
    exim_drop_users = run_cmd("cat /etc/exim_drop_users | grep -v \"^#\"")

    if user not in exim_drop_users:
        current_time = time.strftime("%Y-%m%d-%H%M%S", time.localtime())
        run_cmd(
            f"echo \"{user}: Automatic {current_time}\"  >> /etc/exim_drop_users")
        send_mail("Exim Local Connection Warning",
                  f"該 cPanel 帳號 {user} 因發信數量已達 {count} 封，已超過方案所訂的 {max_mail_per_hour} 封上限\n已自動封鎖到 /etc/exim_drop_users ，請查看 /var/log/exim_mainlog 進行確認。")


def get_user_mailperhour(user: str) -> int:
    if RESELLER:
        return int(DELIVERY_LIMIT)

    max_email_per_hour = run_cmd(
        f"grep \"MAX_EMAIL_PER_HOUR=\" /var/cpanel/users/{user}").split("=")[1]

    if max_email_per_hour in ["unlimited", "0"]:
        return int(DELIVERY_LIMIT)

    return int(max_email_per_hour)


def local_exim_connection_analyzer():
    data_list = []

    if whole_day:
        today = time.strftime("%Y-%m-%d", time.localtime())
    else:
        today = time.strftime("%Y-%m-%d %H", time.localtime())

    exim_mainlog = run_cmd(
        f"grep \"{today}\" /var/log/exim_mainlog | grep \"B=identify_local_connection\|P=local\"")

    for line in exim_mainlog.splitlines():
        user = find_user(line)

        if user in RESERVED_LIST:
            continue

        if "P=local" in line:
            recipients = line[::-1].split(" rof ")[0].count("@")

            for x in range(0, recipients):
                data_list.append(user)
        else:
            data_list.append(user)

    for count, user in sorted(((data_list.count(i), i) for i in set(data_list))):
        if verbose:
            print(f"{user}: {count}")

        if count <= DELIVERY_LIMIT:
            continue

        max_mail_per_hour = get_user_mailperhour(user)

        if count > max_mail_per_hour and drop:
            drop_user(user, count, max_mail_per_hour)


if __name__ == "__main__":
    verbose = True
    drop = False
    whole_day = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-q" in sys.argv:
        verbose = False
    if "-f" in sys.argv:
        drop = True
    if "-w" in sys.argv:
        whole_day = True

    local_exim_connection_analyzer()

