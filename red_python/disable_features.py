#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/03/15
# Author: Red Shen <red@host.com.tw>
import os, sys
import json

#Note: use 'whmapi1 getfeaturelist' to get the feature names. 
FEATURES_TO_BE_DISABLED = ["ssh"]

def get_cmd_output(command):
    #print(command)
    return os.popen(command).read().strip()
    
def disable_features():
    raw_data = get_cmd_output("whmapi1 get_available_featurelists --output=json")
    json_data = json.loads(raw_data)
    
    if len(sys.argv) >= 2:
        feature_list = []
        
        for x in range(1, len(sys.argv)):
            feature_list.append(sys.argv[x])

    else:
        feature_list = FEATURES_TO_BE_DISABLED


    if json_data["metadata"]["result"] == 1:
        for featurelist in json_data["data"]["available_featurelists"]:
            #print(featurelist)
            for feature in feature_list:
                cmd = "whmapi1 update_featurelist featurelist=\"{0}\" \"{1}\"=0 --output=json".format(featurelist, feature)
                os.system(cmd)

if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    disable_features()

