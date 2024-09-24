#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/10/19
# Author: Red Shen <red@host.com.tw>
import os, sys

LOCAL_DOMAIN = "/etc/localdomains"
REMOTE_DOMAIN = "/etc/remotedomains"

def run_cmd(command, display = False):
    if display:
        print(command)

    return os.popen(command).read().strip()
    
def get_list(input_path):
    data_list = []

    if os.path.isfile(input_path):
        input_file = open(input_path, "r")
        for line in input_file.readlines():
            if "#" not in line and line.strip() != "":
                data_list.append(line.strip())

    return data_list
    
def find_registar(domain):
    whois = run_cmd("whois {0}|grep \"Registrar:\|Registration Service Provider:\"".format(domain))
    if whois != "":
        return whois.split(":")[1].strip()
    else:
        return whois
    
def list_domain_mx():
    if "--local" in sys.argv:
        domain_list = get_list(LOCAL_DOMAIN)
    elif "--remote" in sys.argv:
        domain_list = get_list(REMOTE_DOMAIN)
    else:
        domain_list = get_list(LOCAL_DOMAIN)
        
    for domain in domain_list:
        mx = " ".join(run_cmd("dig +short MX {0}".format(domain)).split())
        ns = " ".join(run_cmd("dig +short NS {0}".format(domain)).split())
        print("{0}: {1}: {2}".format(domain, mx, ns))

if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    list_domain_mx()

