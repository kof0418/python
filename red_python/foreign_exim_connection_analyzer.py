#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2019/12/17
# Author: Red Shen <red@host.com.tw>
# This script will also check the SMTP connections from the server's own IP addresses. Sorry for the confusion of the script naming.
# 2024/01/24
# Modified by Adwin Xie
import os
import re
import smtplib
import socket
import subprocess
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.version_info >= (3, 4):
    from html import escape
else:
    from cgi import escape

with open("/etc/excludesenderdomains", "r", encoding="utf8") as f:
    RESERVED_LIST = f.read().splitlines()

RESELLER = False
EMAIL_NOTIFICATION = True
RECIPIENT = "abuse@twnoc.net"
DELIVERY_LIMIT = 100
MAX_DELIVERY_LIMIT = 300


def run_cmd(command: str, display: bool = False) -> str:
    if display:
        print(command)

    result = subprocess.run(command, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()


def send_mail(subject: str, body: str) -> None:
    if EMAIL_NOTIFICATION:
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
    user = re.findall(r" A=dovecot_(login|plain):(.*?) ", text)
    if len(user) == 0:
        return ""

    user = user[0][1]

    if "@" not in user:
        return ""

    return user


def drop_user(email_account: str, count: int, max_mail_per_hour: int) -> None:
    outgoing_mail_suspended_users = run_cmd(
        "cat /etc/outgoing_mail_suspended_users")
    domain = email_account.split("@")[1]

    if domain in RESERVED_LIST:
        return ""

    if email_account not in outgoing_mail_suspended_users:
        domain = email_account.split("@")[1]
        user = run_cmd(f"/scripts/whoowns {domain}")
        run_cmd(
            f"uapi --user={user} Email suspend_outgoing email={email_account} --output=json")
        send_mail("Exim Foreign Connection Warning",
                  f"該電子信箱帳號 {email_account} 因發信數量已達 {count} 封，已超過方案所訂的 {max_mail_per_hour} 封上限\n已自動封鎖發信功能，請查看 /var/log/exim_mainlog 進行確認。")


def get_user_mailperhour(address: str) -> int:
    if RESELLER:
        return int(DELIVERY_LIMIT)

    domain = address.split("@")[1]
    user = run_cmd(f"/scripts/whoowns {domain}")

    max_email_per_hour = run_cmd(
        f"grep \"MAX_EMAIL_PER_HOUR=\" /var/cpanel/users/{user}").split("=")[1]

    if max_email_per_hour in ["unlimited", "0"]:
        return int(DELIVERY_LIMIT)

    return int(max_email_per_hour)


def foreign_exim_connection_analyzer():
    data_list = []
    user_list = {}

    if whole_day:
        today = time.strftime("%Y-%m-%d", time.localtime())
    else:
        today = time.strftime("%Y-%m-%d %H", time.localtime())

    exim_mainlog = run_cmd(
        f"grep \"{today}\" /var/log/exim_mainlog | grep \"A=dovecot_login:\|A=dovecot_plain:\"")

    for line in exim_mainlog.splitlines():
        if "rejected RCPT" in line:
            continue

        user = find_user(line)

        if user != "":
            recipients = line[::-1].split(" rof ")[0].count("@")

            for x in range(0, recipients):
                data_list.append(user)

    for count, user in sorted(((data_list.count(i), i) for i in set(data_list))):

        if user not in user_list:
            user_list[user] = count
        else:
            user_list[user] = user_list[user] + count

        if verbose:
            print(f"{user}: {count}")

    if len(data_list) != 0 and verbose:
        print("\nTotal:")

    for address, count in user_list.items():
        if verbose:
            print("{0}: {1} ".format(address, count))

        if count <= DELIVERY_LIMIT:
            continue

        max_email_per_hour = get_user_mailperhour(address)

        if count > max_email_per_hour and drop:
            drop_user(address, count, max_email_per_hour)


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

    foreign_exim_connection_analyzer()

