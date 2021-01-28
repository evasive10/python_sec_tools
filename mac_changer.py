#!/usr/bin/python3

import argparse
import subprocess
import re
from os import listdir

avail_interfaces = listdir("/sys/class/net/")

def get_arguments():
    parser = argparse.ArgumentParser(description="Changes MAC address of a given interface")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("interface", type=str, help="Specifies interface to use")
    parser.add_argument("mac", type=str, help="Desired new MAC address (must be in 00:00:00:00:00:00 form)")
    return parser.parse_args()


def mac_change(interface, new_mac, avail_interfaces):
    if interface.isalnum():
        if interface in avail_interfaces:
            print(f"[+] Changing MAC address for {interface} to {new_mac}\n")
            subprocess.run(["ifconfig", interface, "down"])
            subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
            subprocess.run(["ifconfig", interface, "up"])
        else:
            print("[-] Please select interface from: " + ", " .join(avail_interfaces))
    else:
        print("[-] Please select a valid interface")


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode("utf-8")

    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not find a MAC address.")

args = get_arguments()

current_mac = get_current_mac(args.interface)
print(f"[+] Current MAC address: {current_mac}\n")

mac_change(args.interface, args.mac, avail_interfaces)

current_mac = get_current_mac(args.interface)
if current_mac == args.mac:
    print(f"[+] MAC address successfully chnaged to {current_mac}")
else:
    print("[-] MAC address was not changed")
