#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import time
import apifunctions

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
gregory_dunlap/celticcow

sync cma groups
"""

"""
move this to apifunction lib in future
"""
def login_api(key, mds, domain):
    payload = {"api-key" : key, "domain" : domain}
    response = apifunctions.api_call(mds, "login", payload, "")

    return response["sid"]
#end of api

def get_cma_contents(mds_ip, cma_ip, group_name):
    debug = 1

    key = {}
    with open('apirw-key.json', 'r') as f:
        key = json.load(f)
        
        if(debug == 1):
            print(key)
            print(key['api-key'])
    
    sid = ""
    try:
        sid = login_api(key['api-key'], mds_ip, cma_ip)
        if(debug == 1):
            print("session id : " + sid)

        # do stuff here

        time.sleep(5)
        logout_result = apifunctions.api_call(mds_ip, "logout", {}, sid)
        if(debug == 1):
            print(logout_result)

    except:
        print("error with login")
        if(sid != ""):
            emergency_logout = apifunctions.api_call(mds_ip, "logout", {}, sid)

def main():
    print("begin")
    mds_ip = "146.18.96.16"
    cma1 = "146.18.96.25"

    get_cma_contents(mds_ip, cma1, "cute-networks")

    


if __name__ == "__main__":
    main()
#end of program