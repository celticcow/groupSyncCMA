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

def parse_host(host_json):
    debug = 1

    print("host", end=",")
    print(host_json['name'], end=",")
    print(host_json['ipv4-address'], end="\n")

def parse_address_range(range_json):
    debug = 1

    print("address-range", end=",")
    print(range_json['name'], end=",")
    print(range_json['ipv4-address-first'], end=",")
    print(range_json['ipv4-address-last'], end="\n")

def parse_network(network_json):
    debug = 1

    print("network", end=",")
    print(network_json['name'], end=",")
    print(network_json['subnet4'], end=",")
    print(network_json['subnet-mask'], end="\n")

def get_group_contents(mds_ip, cma_sid, group_name):
    debug = 0

    # do stuff here
    try:
        group_info_response = apifunctions.api_call(mds_ip, "show-group", {"name" : group_name}, cma_sid)

        if(debug == 1):
            print(group_info_response)

            print("***********************************")
            print(group_info_response['members'])

        for i in range(len(group_info_response['members'])):
            #print(group_info_response['members'][i])
            
            if(group_info_response['members'][i]['type'] == "host"):
                parse_host(group_info_response['members'][i])
            
            elif(group_info_response['members'][i]['type'] == "network"):
                parse_network(group_info_response['members'][i])
            
            elif(group_info_response['members'][i]['type'] == "address-range"):
                parse_address_range(group_info_response['members'][i])

            elif(group_info_response['members'][i]['type'] == "group"):
                if(debug == 1):
                    print("group found", end=" ")
                    print(group_info_response['members'][i]['name'])
                get_group_contents(mds_ip, cma_sid, group_info_response['members'][i]['name'])
            
            else:
                print("unknown group memeber")
                print(group_info_response['members'][i]['type'])
                print(group_info_response['members'][i]['name'])
            #print("\n---------")
    except:
        print("error getting group data")
        

def main():
    debug = 0
    ##print("begin")
    mds_ip = "146.18.96.16"
    cma1 = "146.18.96.25"

    key = {}
    with open('apirw-key.json', 'r') as f:
        key = json.load(f)
        
        if(debug == 1):
            print(key)
            print(key['api-key'])
    
    sid = ""
    try:
        sid = login_api(key['api-key'], mds_ip, cma1)
        if(debug == 1):
            print("session id : " + sid)

        get_group_contents(mds_ip, sid, "cute_networks")

        time.sleep(5)
        logout_result = apifunctions.api_call(mds_ip, "logout", {}, sid)
        if(debug == 1):
            print(logout_result)

    except:
        print("error with login")
        if(sid != ""):
            emergency_logout = apifunctions.api_call(mds_ip, "logout", {}, sid)
#end of main


if __name__ == "__main__":
    main()
#end of program