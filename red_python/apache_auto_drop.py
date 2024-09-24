#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/02/14
# Author: Red Shen <red@host.com.tw>
import os, sys
import time
import shlex

POST_KEYWORD_LIST = ["xmlrpc.php", "wp-login.php"]
GET_KEYWORD_LIST = ["/forum/"]
COUNTRY_WHITELIST = ["Address not found", "Taiwan",  "United States"]
COUNTRY_BLACKLIST = ["China"]
INTERVAL = 5
METHOD = "GET"

def get_cmd_output(command):
    #print(command)
    return os.popen(command).read().strip()
    
def run_cmd(cmd, quiet = True):
    if quiet == True:
        cmd = cmd + " >/dev/null 2>&1"

    os.system(cmd)
    
def get_ip_country(ip):
    geoip = get_cmd_output("/usr/bin/geoiplookup {0}".format(ip))
    return geoip.splitlines()[0].replace("GeoIP Country Edition:", "").strip()

def get_time():
    now = time.localtime()
    hour = time.strftime("%H", now)
    return int(hour)

def apache_auto_drop(auto):
    drop = False
    status = get_cmd_output("/usr/sbin/apachectl fullstatus")
    dropped_ip = []
    
    if auto:
        drop = True
    elif len(sys.argv) >= 2 and sys.argv[1] == "--drop":
        drop = True
    
    for line in status.splitlines():
        match = False

        if METHOD == "POST" and "POST" in line and any(keyword in line for keyword in POST_KEYWORD_LIST):
            match = True
        elif METHOD == "GET" and "GET" in line and any(keyword in line for keyword in GET_KEYWORD_LIST):
            match = True
        
        if match == True:
            items = shlex.split(line)
            
            if len(items) < 16:
                return False
            
            ip = items[11]
            method = items[14]
            path = items[15]
            country = get_ip_country(ip)
            listed = False
            
            if any(code in country for code in COUNTRY_BLACKLIST):
                listed = True
            elif not any(code in country for code in COUNTRY_WHITELIST):
                listed = True
            
            if listed == True:
                if not auto:
                    print("{0}: {1}: {2}".format(ip, country, path))
                
                if drop == True and ip not in dropped_ip:
                    run_cmd("/usr/sbin/csf -d {0} \"{1} {2} from {3}\"".format(ip, method, path, country))
                    dropped_ip.append(ip)
            else:
                if not auto:
                    print("{0}: {1}: {2} whitelisted".format(ip, country, path))
                
def main_loop():
    if len(sys.argv) >= 3 and sys.argv[1] == "-t" and sys.argv[2].isdigit():
        end_time = int(sys.argv[2])
        
        while True:
            if get_time() >= end_time:
                break
                
            apache_auto_drop(True)
            time.sleep(INTERVAL)
    else:
        apache_auto_drop(False)
                
if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    main_loop()

