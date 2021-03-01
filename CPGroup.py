#!/usr/bin/python3

class CPRange(object):
    """
    """
    def __init__(self, name="default", start_ip="0.0.0.0", end_ip="255.255.255.255"):
        self.name = name
        self.start_ip = start_ip
        self.end_ip = end_ip
    
    def get_name(self):
        return(self.name)
    
    def get_start_ip(self):
        return(self.start_ip)
    
    def get_end_ip(self):
        return(self.end_ip)
    
    def set_name(self, name):
        self.name = name
    
    def set_start_ip(self, start_ip):
        self.start_ip = start_ip
    
    def set_end_ip(self, end_ip):
        self.end_ip = end_ip

class CPHost(object):
    """
    """
    def __init__(self, name="default", ip_addr="127.0.0.1"):
        self.name = name
        self.ip_addr = ip_addr
    
    def get_name(self):
        return(self.name)
    
    def get_ip_addr(self):
        return(self.ip_addr)
    
    def set_name(self, name):
        self.name = name
    
    def set_ip_addr(self, ip_addr):
        self.ip_addr = ip_addr
#end of CPHost

class CPNetwork(object):
    """
    """
    def __init__(self, name="default", network="0.0.0.0", netmask="255.255.255.255"):
        self.name = name
        self.network = network
        self.netmask = netmask
    
    def get_name(self):
        return(self.name)
    
    def get_network(self):
        return(self.network)
    
    def get_netmask(self):
        return(self.netmask)
    
    def set_name(self, name):
        self.name = name
    
    def set_network(self, network):
        self.network = network
    
    def set_netmask(self, netmask):
        self.netmask = netmask

#end of class CPNetwork


class CPGroup(object):
    """
    list of hosts / networks / address-ranges
    """

    def __init__(self, name="defualt"):
        self.name = name
        self.hosts = list()
        self.networks = list()
        self.addr_ranges = list()

    def add_host(self, CPHost_obj):
        self.hosts.append(CPHost_obj)
    
    def add_network(self, CPNetwork_obj):
        self.networks.append(CPNetwork_obj)
    
    def add_range(self, CPRange_obj):
        self.addr_ranges.append(CPRange_obj)
    
    def get_hosts(self):
        return(self.hosts)
    
    def get_networks(self):
        return(self.networks)
    
    def get_addr_range(self):
        return(self.addr_ranges)
    
    def get_net_len(self):
        return(len(self.networks))

#end of class CPGroup