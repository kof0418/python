#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/06/25
# Author: Red Shen <red@host.com.tw>
import os, sys
import time
import shlex

KEYWORD_LIST = ["xmlrpc.php", "wp-login.php"]
COUNTRY_WHITELIST = ["Address not found", "Taiwan"]
COUNTRY_GREYLIST = []
IP_REVERSE_WHITELIST = ["google", "cloudfront", "uptimerobot.com"]
CRITICAL_AMOUNT = 6
MODERATELY_AMOUNT = 100
APACHE_LOG_PATH = "/usr/local/apache/domlogs/"
IPSET = "wordpress"
INTERVAL = 4
CSF_MODE = True

def get_cmd_output(command):
    #print(command)
    return os.popen(command).read().strip()
    
def run_cmd(cmd, silence = True):
    if silence == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)
    
def get_ip_country(ip):
    '''
    if ":" in ip:
        geoip = get_cmd_output("/usr/bin/geoiplookup6 {0}".format(ip))
    else:
        geoip = get_cmd_output("/usr/bin/geoiplookup {0}".format(ip))
    '''
    geoip = get_cmd_output("/usr/bin/geoiplookup {0}".format(ip))

    return geoip.splitlines()[0].replace("GeoIP Country Edition:", "").replace("GeoIP Country V6 Edition:", "").strip()

def get_ip_blacklisted(ip):
    reverse_ip = get_cmd_output("/usr/bin/dig +short -x {0}".format(ip))
    
    for keyword in IP_REVERSE_WHITELIST:
        if keyword in reverse_ip:
            return False

    return True

def get_tries(ip, path):
    now = time.localtime()
    today = time.strftime("%d/%b/%Y", now)
    grep_result = get_cmd_output("nice -n 19 grep -Ehr \"{0}.*{1}.*POST.*{2}.* 200 \" {3}|wc -l".format(ip, today, path, APACHE_LOG_PATH))

    if grep_result.isdigit():
        return int(grep_result)
    else:
        return -1

def wordpress_drop(drop):
    status = get_cmd_output("/usr/sbin/apachectl fullstatus")
    dropped_ip = []
    
    for line in status.splitlines():
        if "POST" in line and any(keyword in line for keyword in KEYWORD_LIST):
            items = shlex.split(line)
            
            if len(items) < 16:
                continue
            
            ip = items[11]
            method = items[14]
            path = items[15]
            country = get_ip_country(ip)
            allowed_tries = 0
            
            if ip in dropped_ip:
                continue

            if any(code in country for code in COUNTRY_GREYLIST):
                allowed_tries = MODERATELY_AMOUNT
            elif not any(code in country for code in COUNTRY_WHITELIST):
                allowed_tries = CRITICAL_AMOUNT

            tries = get_tries(ip, path)

            if allowed_tries != 0 and tries >= allowed_tries and get_ip_blacklisted(ip):
                if not quiet:
                    print("{0}: {1}: {2} ({3})".format(ip, country, path, tries))
                
                if drop == True:
                    if CSF_MODE == False:
                        run_cmd("/usr/sbin/ipset add {0} {1} -exist".format(IPSET, ip))
                    elif CSF_MODE == True:
                        run_cmd("/usr/sbin/csf -d {0} \" {1} from {2}\"".format(ip, path, country))

                    dropped_ip.append(ip)
            else:
                if not quiet:
                    print("{0}: {1}: {2} ({3}) passed".format(ip, country, path, tries))
                
def main_loop():
    if len(sys.argv) >= 2:
        if sys.argv[1] == "--infinite":
            while True:
                wordpress_drop(True)
                time.sleep(INTERVAL)
        elif sys.argv[1] == "--drop":
            wordpress_drop(True)
    else:
        wordpress_drop(False)
                
if __name__ == "__main__":
    quiet = False
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "--quiet" in sys.argv:
        quiet = True

    main_loop()

