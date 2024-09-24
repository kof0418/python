#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/11/22
# Author: Red Shen <red@host.com.tw>
# https://developers.google.com/safe-browsing/v4/lookup-api
import os, sys
import json

POST_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=API_KEY"
API_KEY_LOCATION = ".google.api.key"
DOMAIN_LOCATION = "/etc/userdomains"
MAX_DOMAINS = 500

def is_python3():
    if (sys.version_info > (3, 0)):
        return True
    else:
        return False

def get_api_key():
    api_key = ""

    if os.path.isfile(API_KEY_LOCATION):
        keyfile = open(API_KEY_LOCATION, "r")
        api_key = keyfile.read().strip()
        keyfile.close()

    return api_key

def get_domain_list():
    domain_list = []
    
    if os.path.isfile(DOMAIN_LOCATION):
        domain_file = open(DOMAIN_LOCATION , "r")

        for line in domain_file.read().splitlines():
            if ":" not in line:
                continue

            domain = line.split(":")[0]

            if "*" not in domain:
                domain_list.append(domain)

        domain_file.close()

    return domain_list

def divide_chunks(input_list, number): 
    for i in range(0, len(input_list), number):  
        yield input_list[i:i + number]

def create_data(chunk):
    request_data = {}
    url_list = []
    request_data["client"] = {}
    request_data["threatInfo"] = {}
    request_data["client"]["clientId"] = "twnoc"
    request_data["client"]["clientVersion"] = "1.0.0"
    request_data["threatInfo"]["threatTypes"] = ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION"]
    request_data["threatInfo"]["platformTypes"] = ["ANY_PLATFORM"]
    request_data["threatInfo"]["threatEntryTypes"] = ["URL"]

    for url in chunk:
        url_list.append({"url": url})

    request_data["threatInfo"]["threatEntries"] = url_list 
    #print(json.dumps(request_data, indent=4, sort_keys=True))
    return request_data

def send_request(post_url, chunk):
    if verbose:
        print("Sending the request ({0} domains).".format(len(chunk)))

    request_data = create_data(chunk)
    request = Request(post_url)
    request.add_header("Content-Type", "application/json")
    json_data = json.dumps(request_data)

    if python3:
        json_data = json_data.encode("utf-8")

    try:
        return urlopen(request, json_data)

    except URLError as error:
        error_msg = error.read()
        
        if python3:
            error_msg = error_msg.decode("utf-8")

        print(error_msg)
        return None

def print_response(response):
    if response == None:
        return False

    content = response.read()

    if python3:
        content = content.decode("utf-8")

    if len(content) <= 3:
        return True
    
    if verbose:
        print(content)
    else:
        formatting_response(content)

def formatting_response(content):
    data = json.loads(content)

    for item in data["matches"]:
        print("threatType: {0}".format(item["threatType"]))
        print("platformType: {0}".format(item["platformType"]))
        print("threatEntryType: {0}".format(item["threatEntryType"]))
        print("url: {0}".format(item["threat"]["url"]))
        print("")

def safe_browsing_check():
    api_key = get_api_key()

    if api_key == "":
        print("Can't find the API key, abort.")
        return False

    post_url = POST_URL.replace("API_KEY", api_key)
    domain_list = get_domain_list()
    split_list = list(divide_chunks(domain_list, MAX_DOMAINS))

    for chunk in split_list:
        print_response(send_request(post_url, chunk))

if __name__ == "__main__":
    verbose = False
    python3 = is_python3()

    if python3:
        from urllib.request import *
        from urllib.error import *
    else:
        from urllib2 import *

    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)

    if "-v" in sys.argv:
        verbose = True

    safe_browsing_check()

