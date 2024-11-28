#!/usr/bin/python3

"""
---------------------------------------
Can change system's MAC-Address and local IP.
GNU/Linux supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

try:
    import re
    import os
    import usr
    import random
    import subprocess
    from sys import exit
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")
    exit(1)


def get_valid_interfaces() -> list:
    try:
        interfaces: list = os.listdir("/sys/class/net")
        valid_interfaces: list = [interface for interface in interfaces if os.path.islink(f"/sys/class/net/{interface}")]
        return valid_interfaces
    except FileNotFoundError:
        print(f"{RED}[!] Error: /sys/class/net directory not found.{RESET}")
        return []


def change_mac() -> None:
    os.system("clear")

    print("We are going to change the system's MAC address.")
    answer: str = input("[?] Are you sure you want to change the MAC address? (y/N): ").lower()
    if answer not in ["y", "yes"]:
        print(f"{RED}[!] Operation canceled.{RESET}")
        return

    interfaces: list = get_valid_interfaces()
    if not interfaces:
        print(f"{RED}[!] No valid interfaces found. Exiting.{RESET}")
        return

    print(f"Available interfaces: {interfaces}")
    interface: str = input("\n[==>] Enter your interface: ").strip()

    if interface not in interfaces:
        print(f"{RED}[!] Invalid interface. Exiting.{RESET}")
        return

    mac_parts: list = [random.randint(0, 255) for _ in range(6)]
    new_mac: str = ":".join(f"{part:02x}" for part in mac_parts)
    print(f"[*] Your new MAC address: {new_mac}")

    try:
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        
        print(f"\n{GREEN}[*] Success! MAC address changed.{RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"{RED}[!] Error while changing MAC address:\n{error}.{RESET}")


def is_valid_ip(ip: str) -> bool:
    pattern: str = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip) is not None


def change_lan_ip() -> None:
    os.system("clear")
    
    print("We are going to change the local IP address.")
    answer: str = input("[*] Are you sure you want to change the IP address? (y/N): ").lower()
    if answer not in ["y", "yes"]:
        print(f"{RED}[!] Operation canceled.{RESET}")
        return

    interfaces: list = get_valid_interfaces()
    if not interfaces:
        print(f"{RED}[!] No valid interfaces found. Exiting.{RESET}")
        return

    print(f"Available interfaces: {interfaces}")
    interface: str = input("\n[*] Enter your interface: ").strip()

    if interface not in interfaces:
        print(f"{RED}[!] Invalid interface. Exiting.{RESET}")
        return

    new_ip: str = input("[*] Enter the new IP address (e.g., 192.168.1.10): ").strip()
    if not is_valid_ip(new_ip):
        print(f"{RED}[!] Error: Invalid IP address: {new_ip}. Exiting.{RESET}")
        return

    subnet_mask: str = input("[*] Enter the subnet mask (e.g., 255.255.255.0): ").strip()
    if not is_valid_ip(subnet_mask):
        print(f"{RED}[!] Error: Invalid subnet mask: {subnet_mask}. Exiting.{RESET}")
        return

    try:
        subprocess.run(["ip", "addr", "flush", "dev", interface], check=True)
        subprocess.run(["ip", "addr", "add", f"{new_ip}/{subnet_mask}", "dev", interface], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        print("\n{GREEN}[*] Success! IP address changed.{RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"{RED}[!] Error: cant change IP address: {error}.{RESET}")
        print("[*] We will try another way...")
        
        try:
            subprocess.run(["ifconfig", interface, "inet", new_ip, "netmask", subnet_mask], check=True)
            print("\n{GREEN}[*] Success! IP address changed.{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            print(f"{RED}[!] Error: still cant change IP address: {error}.{RESET}")
            

def address_changer() -> None:
    os.system("clear")

    functions: dict = {
        "change_mac": change_mac,
        "change_lan_ip": change_lan_ip
    }

    print("+---- Address Changer ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name: ").lower()
    if your_function in functions:
        functions[your_function]()
