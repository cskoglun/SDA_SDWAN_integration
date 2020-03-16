

import os, sys
from pprint import pprint
from ncclient import manager
import xmltodict
import xml.dom.minidom
import json

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, ".."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)

# Import inventory file
import inventory

device = inventory.BN

def ncclient_connection(xml_data):

    with manager.connect(
        host=device["ip"],
        port="830",
        username=device["username"],
        password=device["password"],
        hostkey_verify=False
        ) as m:
        netconf_reply = m.get(xml_data)

    return netconf_reply

def get_vrf_vlan_map():
    netconf_data = """
    <filter>
        <vrf-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vrf-oper">
            <vrf-entry>
                
            </vrf-entry>
        </vrf-oper-data>
    </filter>
    """
    
    netconf_reply = ncclient_connection(netconf_data)

    data_whole = json.loads(json.dumps(xmltodict.parse(netconf_reply.xml)))
    data = data_whole["rpc-reply"]['data']['vrf-oper-data']['vrf-entry']

    vrf_to_vlan_mapping = {}
    for i in range(0,len(data)):
        vrf_to_vlan_mapping[data[i]['vrf-name']] = data[i]['interface'][0]

    return vrf_to_vlan_mapping


def get_ipv4_vlan_map():

    netconf_data = """
        <filter>
        <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
            <interface>
            <name></name>
            <ipv4/>
            </interface>
        </interfaces>
        </filter>
    """

    netconf_reply = ncclient_connection(netconf_data)

    data_whole = json.loads(json.dumps(xmltodict.parse(netconf_reply.xml)))
    data = data_whole['rpc-reply']['data']['interfaces']['interface']

    vlans_to_ip ={}
    for i in range(0,len(data)):
        if 'ipv4' in data[i]: 
            vlans_to_ip[data[i]['name']] = data[i]['ipv4']

    return vlans_to_ip

vrfs_ = get_vrf_vlan_map()
ipv4_ = get_ipv4_vlan_map()

pprint(ipv4_)
vrf = {}

list_ = vrfs_.items()
print(list_)
 for i in range(0,len(ipv4)):



#print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


# if __name__ == '__main__':
    # pprint(get_vrf_vlan_map())
    # pprint(get_ipv4_vlan_map())
