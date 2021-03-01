#!/usr/bin/python3 -W ignore::DeprecationWarning

import requests
import json
import time
import apifunctions

from CPGroup import CPGroup
from CPGroup import CPHost
from CPGroup import CPNetwork
from CPGroup import CPRange

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

    cphost = CPHost(host_json['name'], host_json['ipv4-address'])
    return(cphost)
#end of parse_host

def parse_address_range(range_json):
    debug = 1

    print("address-range", end=",")
    print(range_json['name'], end=",")
    print(range_json['ipv4-address-first'], end=",")
    print(range_json['ipv4-address-last'], end="\n")

    cprange = CPRange(range_json['name'], range_json['ipv4-address-first'], range_json['ipv4-address-last'])
    return(cprange)
#end of parse_address_range

def parse_network(network_json):
    debug = 1

    print("network", end=",")
    print(network_json['name'], end=",")
    print(network_json['subnet4'], end=",")
    print(network_json['subnet-mask'], end="\n")

    cpnet = CPNetwork(network_json['name'], network_json['subnet4'], network_json['subnet-mask'])
    return(cpnet)
#end of parse_network

def get_group_contents(mds_ip, cma_sid, group_name):
    debug = 0

    orig_group = CPGroup(group_name)

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
                orig_group.add_host(parse_host(group_info_response['members'][i]))
            
            elif(group_info_response['members'][i]['type'] == "network"):
                orig_group.add_network(parse_network(group_info_response['members'][i]))
            
            elif(group_info_response['members'][i]['type'] == "address-range"):
                orig_group.add_range(parse_address_range(group_info_response['members'][i]))

            elif(group_info_response['members'][i]['type'] == "group"):
                if(debug == 1):
                    print("group found", end=" ")
                    print(group_info_response['members'][i]['name'])
                sub_group = get_group_contents(mds_ip, cma_sid, group_info_response['members'][i]['name'])
                nets_to_build   = sub_group.get_networks()
                host_to_build   = sub_group.get_hosts()
                range_to_build  = sub_group.get_addr_range()

                for net in nets_to_build:
                    orig_group.add_network(net)
                for host in host_to_build:
                    orig_group.add_host(host)
                for ip_range in range_to_build:
                    orig_group.add_range(ip_range)
                ## take apart and add to existing orig_group
            
            else:
                print("unknown group memeber")
                print(group_info_response['members'][i]['type'])
                print(group_info_response['members'][i]['name'])
            #print("\n---------")
    except:
        print("error getting group data")
    
    return(orig_group)
#end of get_group_contents
        

def make_group(mds_ip, cma_ip):
    pass

def main():
    debug = 1
    ##print("begin")
    mds_ip = "146.18.96.16"
    cma1 = "146.18.96.25"
    cma2 = "146.18.96.26"

    orig_group_info = CPGroup()

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

        orig_group_info = get_group_contents(mds_ip, sid, "Test-Group")  #cute_networks

        time.sleep(5)
        logout_result = apifunctions.api_call(mds_ip, "logout", {}, sid)
        if(debug == 1):
            print(logout_result)

    except:
        print("error with login")
        if(sid != ""):
            emergency_logout = apifunctions.api_call(mds_ip, "logout", {}, sid)
    
    # we have fetched data now
    print("add to other cma")

    try:
        sid = login_api(key['api-key'], mds_ip, cma2)
        if(debug == 1):
            print("session id : " + sid)
        
        apifunctions.add_a_group(mds_ip, "newgrp", sid)

        nets_to_build = orig_group_info.get_networks()
        host_to_build = orig_group_info.get_hosts()
        range_to_build = orig_group_info.get_addr_range()

        print("---------------------")
        print(len(nets_to_build))
        print(len(host_to_build))
        print(len(range_to_build))
        print("---------------------")
        for net in nets_to_build:
            print(net.get_name())
            print(net.get_network(), end="/")
            print(net.get_netmask())
            #add_a_network_with_group(ip_addr, name, network, netmask, group, sid)
            apifunctions.add_a_network_with_group(mds_ip, net.get_name(), net.get_network(), net.get_netmask(), "newgrp", sid)
            
        for host in host_to_build:
            print(host.get_name())
            print(host.get_ip_addr())
            #(ip_addr, name, ip, group, sid)
            apifunctions.add_a_host_with_group(mds_ip, host.get_name(), host.get_ip_addr(), "newgrp", sid)

        for ip_range in range_to_build:
            print(ip_range.get_name())
            print(ip_range.get_start_ip(), end="-")
            print(ip_range.get_end_ip())
            #add_a_range_with_group(ip_addr, name, startip, endip, group, sid)
            apifunctions.add_a_range_with_group(mds_ip, ip_range.get_name(), ip_range.get_start_ip(), ip_range.get_end_ip(), "newgrp", sid)

        time.sleep(5)

        publish_result = apifunctions.api_call(mds_ip, "publish", {}, sid)
        time.sleep(20)
        print(publish_result)
        time.sleep(5)
        logout_result = apifunctions.api_call(mds_ip, "logout", {}, sid)
        if(debug == 1):
            print(logout_result)
    except:
        print("error with second login")
        if(sid != ""):
            emergency_logout = apifunctions.api_call(mds_ip, "logout", {}, sid)

    


#end of main


if __name__ == "__main__":
    main()
#end of program