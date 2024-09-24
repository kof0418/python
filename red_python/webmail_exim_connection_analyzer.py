#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2019/12/17
# Author: Red Shen <red@host.com.tw>
# Note: default email account will be ignored in the current implementation.
# Modified by: Adwin <adwin@host.com.tw>
import os
import re
import smtplib
import socket
import sys
import subprocess
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.version_info >= (3, 4):
    from html import escape
else:
    from cgi import escape

ROUNDCUBE_CONFIG = "/usr/local/cpanel/base/3rdparty/roundcube/config/config.inc.php"
SQLITE_MODE = True
EMAIL_NOTIFICATION = True
RECIPIENT = "abuse@twnoc.net"
DELIVERY_LIMIT = 100
ROUNDCUBE_LOG_PATH = ""
CPANEL_ACCESS_LOG_PATH = "/usr/local/cpanel/logs/access_log"
DEFAULT_SEARCH_MODE = 1
RESELLER = False


def check_roundcube_dbconfig() -> None:
    global SQLITE_MODE, ROUNDCUBE_LOG_PATH
    config = run_cmd(f"cat {ROUNDCUBE_CONFIG}")

    if "$config['db_dsnw'] = 'sqlite" in config:
        SQLITE_MODE = True
        ROUNDCUBE_LOG_PATH = "/home/*/logs/roundcube/sendmail.log"
    elif "$config['db_dsnw'] = 'mysql" in config:
        SQLITE_MODE = False
        ROUNDCUBE_LOG_PATH = "/var/cpanel/roundcube/log/sendmail.log"


def run_cmd(command: str, display: bool = False) -> str:
    if display:
        print(command)

    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        if "No such file or directory" in result.stderr.decode("utf-8"):
            return ""

    return result.stdout.decode("utf-8").strip()


def send_mail(subject: str, body: str) -> None:
    if EMAIL_NOTIFICATION is False:
        return False

    hostname = socket.gethostname()
    sender = f"root@{hostname}"
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


def regex_search(text: str, regex: str) -> str:
    result = re.findall(regex, text)

    if len(result) >= 1:
        return result[0]
    else:
        return ""


def find_user(text: str) -> str:
    if search_mode == 1:
        ip = regex_search(text, r" \[(.*?)\];")
        user = regex_search(text, r" User (.*?) ")
    else:
        items = text.split()
        ip = items[0]
        user = items[2].replace("%40", "@")

    if "@" in user and ip != "":
        return f"{user} {ip}"
    else:
        return ""


def drop_user(email_account: str, count: int, max_mail_per_hour: int) -> None:
    outgoing_mail_suspended_users = run_cmd("cat /etc/outgoing_mail_suspended_users")

    if email_account not in outgoing_mail_suspended_users:
        domain = email_account.split("@")[1]
        user = run_cmd(f"/scripts/whoowns {domain}")
        run_cmd(
            f"uapi --user={user} Email suspend_outgoing email={email_account} --output=json"
        )

        if search_mode == 1 and SQLITE_MODE is False:
            log_path = ROUNDCUBE_LOG_PATH
        elif search_mode == 1 and SQLITE_MODE is True:
            log_path = ROUNDCUBE_LOG_PATH.replace("*", user)
        else:
            log_path = CPANEL_ACCESS_LOG_PATH

        send_mail(
            "Exim Webmail Connection Warning",
            f"該電子信箱帳號 {email_account} 因發信數量已達 {count} 封，已超過方案所訂的 {max_mail_per_hour} 封上限\n系統已自動封鎖發信功能，請查看 {log_path} 進行確認",
        )


def get_user_mailperhour(email_account: str) -> int:
    if RESELLER:
        return int(DELIVERY_LIMIT)

    domain = email_account.split("@")[1]
    user = run_cmd(f"/scripts/whoowns {domain}")

    max_email_per_hour = run_cmd(
        f'grep "MAX_EMAIL_PER_HOUR=" /var/cpanel/users/{user}'
    ).split("=")[1]

    if max_email_per_hour in ["unlimited", "0"]:
        return int(DELIVERY_LIMIT)

    return int(max_email_per_hour)


def webmail_exim_connection_analyzer():
    check_roundcube_dbconfig()
    data_list = []
    user_list = {}

    if search_mode == 1:
        today = datetime.now()
    else:
        today = datetime.now() - timedelta(hours=8)

    if whole_day:
        if search_mode == 1:
            today_formatted = today.strftime("%d-%b-%Y")
        else:
            today_formatted = today.strftime("%m/%d/%Y")
    else:
        if search_mode == 1:
            today_formatted = today.strftime("%d-%b-%Y %H")
        else:
            today_formatted = today.strftime("%m/%d/%Y:%H")

    if search_mode == 1:
        input_log = run_cmd(f'grep -ah "{today_formatted}" {ROUNDCUBE_LOG_PATH}')
    else:
        input_log = run_cmd(
            f'grep -a "{today_formatted}.*POST.*framed=1.*mail\&_action=compose" {CPANEL_ACCESS_LOG_PATH}'
        )

    for line in input_log.splitlines():
        user = find_user(line)

        if user != "":
            if search_mode == 1:
                for x in range(0, line.count("@") - 2):
                    data_list.append(user)
            else:
                data_list.append(user)

    for count, user in sorted(((data_list.count(i), i) for i in set(data_list))):
        address, ip = user.split()

        if address not in user_list:
            user_list[address] = count
        else:
            user_list[address] = user_list[address] + count

        if verbose:
            print("{0}: {1}".format(user, count))

    if len(data_list) != 0 and verbose:
        print("\nTotal:")

    for address, count in user_list.items():
        if verbose:
            print(f"{address}: {count} ")

        max_email_per_hour = get_user_mailperhour(address)

        if count > max_email_per_hour and drop:
            drop_user(address, count, max_email_per_hour)


if __name__ == "__main__":
    verbose = True
    drop = False
    whole_day = False
    search_mode = DEFAULT_SEARCH_MODE
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-q" in sys.argv:
        verbose = False
    if "-f" in sys.argv:
        drop = True
    if "-w" in sys.argv:
        whole_day = True
    if "-a" in sys.argv:
        search_mode = 0

    webmail_exim_connection_analyzer()

