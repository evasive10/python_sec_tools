#!/usr/bin/python3

import argparse
import scapy.all as scapy

def scan(ip):
    arp_req = scapy.ARP()
    arp_req.pdst = ip
    broadcast = scapy.Ether()
    broadcast.dst = "ff:ff:ff:ff:ff:ff"
    arp_req_broadcast = broadcast/arp_req
    answered_list = scapy.srp(arp_req_broadcast, timeout=1)[0]
    
    client_list =[]
    for x in answered_list:
        client_dict = {"ip": x[1].psrc, "MAC": x[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_result(result_list):
    print("IP\t\t\t MAC Address")
    print("-" * 80)
    for client in result_list:
        print(client["ip"] + "\t\t" + client["MAC"])



def get_args():
    parser = argparse.ArgumentParser(description="Network scanner")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("target", help="IP or IP range to scan")
    return parser.parse_args()

args = get_args()
scan_result = scan(args.target)
print_result(scan_result)

