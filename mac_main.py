#!/usr/bin/env python3

import subprocess
import optparse
import re
import random


def random_mac():
    digits = '01234567890123456789012345678901234567890123456789012345678901234567890123456789' \
                 '012345678901234567890123456789012345678901234567890123456789abcdefghijklmnpqrstuvwxyz'
    random_picks = []

    for i in range(12):
        random_picks.append(random.choice(digits))

    random_picks = ''.join(random_picks)
    random_picks = re.findall('..', random_picks)

    new_random_mac = ''
    counter = 0
    for i in range(6):
        new_random_mac += random_picks[counter] + ":"
        counter += 1

    return new_random_mac[:-1]


def get_args():
    """
    get input from user
    :return:
    """
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address.")
    parse.add_option("-m", "--mac", dest="new_mac", help="New MAC address to be changed to.")
    opt, arg = parse.parse_args()

    if not opt.interface:
        parse.error("[-] Invalid interface, use --help for more information.")
    elif not opt.new_mac:
        parse.error("[-] Invalid MAC address, use --help for more information.")
    else:
        return opt


def change_mac(interface, new_mac):
    """
    change computer MAC address
    :param interface:
    :param new_mac:
    :return:
    """
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", interface])
    subprocess.call(["ifconfig", interface, "up"])


def current_mac_getter(interface):
    """
    return current mac address
    :param interface:
    :return:
    """
    check = subprocess.check_output(["ifconfig", interface])
    check_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(check))

    if check_result:
        return check_result.group(0)
    else:
        return "[-] Failed to read MAC address."


# GET USER INPUT
options = get_args()

# SHOW CURRENT MAC ADDRESS
current_mac = current_mac_getter(options.interface)
print(f"[+] MAC is: {current_mac}")

# CHANGE MAC ADDRESS
change_mac(options.interface, options.new_mac)
current_mac = current_mac_getter(options.interface)

if current_mac == options.new_mac:
    print(f"[+] MAC IS NOW: {current_mac}")
else:
    print(f"[-] CHANGE FAILED, MAC STILL IS: {current_mac}")
