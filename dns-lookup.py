#!/usr/bin/env python3

import socket
import sys
import struct

try:
    import pyfiglet
except ImportError:
    print("Missing required package: pyfiglet")
    print("Install it with: pip install pyfiglet")
    sys.exit(1)


def print_banner():
    banner = pyfiglet.figlet_format("DNS Lookup", font="slant")
    print("\033[96m" + banner + "\033[0m")
    print("\033[93m  DNS & Network Information Tool\033[0m")
    print("\033[90m  Look up DNS records, resolve hostnames,\033[0m")
    print("\033[90m  and view your network details.\033[0m")
    print()
    print("\033[90m  ─────────────────────────────────────────────\033[0m")
    print()


def print_success(msg):
    print(f"\033[92m  [+] {msg}\033[0m")


def print_info(msg):
    print(f"\033[94m  [*] {msg}\033[0m")


def print_warn(msg):
    print(f"\033[93m  [!] {msg}\033[0m")


def print_error(msg):
    print(f"\033[91m  [-] {msg}\033[0m")


def print_header(msg):
    print(f"\n\033[96m  [{msg}]\033[0m")


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def get_hostname_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return None


def get_all_ips_for_host(hostname):
    try:
        results = socket.getaddrinfo(hostname, None)
        ips = set()
        for result in results:
            family, _, _, _, sockaddr = result
            ip = sockaddr[0]
            label = "IPv4" if family == socket.AF_INET else "IPv6"
            ips.add((ip, label))
        return sorted(ips, key=lambda x: (x[1], x[0]))
    except socket.gaierror:
        return []


def resolve_hostname(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        return None


def reverse_lookup(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror):
        return None


def get_fqdn():
    try:
        return socket.getfqdn()
    except Exception:
        return None


def show_my_network_info():
    print_header("Your Network Information")
    print()

    hostname = socket.gethostname()
    print_info(f"Hostname:       {hostname}")

    fqdn = get_fqdn()
    if fqdn and fqdn != hostname:
        print_info(f"FQDN:           {fqdn}")

    hostname_ip = get_hostname_ip()
    if hostname_ip:
        print_success(f"DNS IP:         {hostname_ip}")
    else:
        print_error("DNS IP:         Could not resolve")

    local_ip = get_local_ip()
    if local_ip:
        print_success(f"Local IP:       {local_ip}")
    else:
        print_error("Local IP:       Could not determine")

    if hostname_ip and local_ip and hostname_ip != local_ip:
        print_warn(f"Note: DNS IP and Local IP differ")

    all_ips = get_all_ips_for_host(hostname)
    if len(all_ips) > 1:
        print()
        print_info("All addresses for this host:")
        for ip, label in all_ips:
            print(f"\033[90m    {label:>4}  {ip}\033[0m")

    if hostname_ip:
        reverse = reverse_lookup(hostname_ip)
        if reverse:
            print()
            print_info(f"Reverse DNS:    {reverse}")


def lookup_hostname(hostname):
    print_header(f"Lookup: {hostname}")
    print()

    ip = resolve_hostname(hostname)
    if ip:
        print_success(f"Resolved:  {hostname} -> {ip}")
    else:
        print_error(f"Could not resolve: {hostname}")
        return

    all_ips = get_all_ips_for_host(hostname)
    if len(all_ips) > 1:
        print()
        print_info("All addresses:")
        for addr, label in all_ips:
            print(f"\033[90m    {label:>4}  {addr}\033[0m")

    reverse = reverse_lookup(ip)
    if reverse:
        print_info(f"Reverse DNS:   {reverse}")


def lookup_ip(ip):
    print_header(f"Reverse Lookup: {ip}")
    print()

    hostname = reverse_lookup(ip)
    if hostname:
        print_success(f"Resolved:  {ip} -> {hostname}")
        forward_ip = resolve_hostname(hostname)
        if forward_ip:
            print_info(f"Forward:   {hostname} -> {forward_ip}")
            if forward_ip == ip:
                print_success("Forward and reverse DNS match")
            else:
                print_warn("Forward and reverse DNS do NOT match")
    else:
        print_error(f"No reverse DNS record for: {ip}")


def batch_lookup():
    filepath = input("\033[97m  Enter path to file (one hostname per line): \033[0m").strip()
    if not filepath:
        print_error("No file path entered.")
        return

    try:
        with open(filepath, "r") as f:
            hosts = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print_error(f"File not found: {filepath}")
        return

    if not hosts:
        print_error("File is empty.")
        return

    print_header(f"Batch Lookup ({len(hosts)} entries)")
    print()

    resolved = 0
    failed = 0

    print(f"\033[90m  {'Hostname':<40} {'IP Address':<18} {'Status'}\033[0m")
    print(f"\033[90m  {'─' * 40} {'─' * 18} {'─' * 8}\033[0m")

    for host in hosts:
        ip = resolve_hostname(host)
        if ip:
            print(f"\033[37m  {host:<40} {ip:<18} \033[92mOK\033[0m")
            resolved += 1
        else:
            print(f"\033[37m  {host:<40} {'-':<18} \033[91mFAIL\033[0m")
            failed += 1

    print()
    print_success(f"Resolved: {resolved}")
    if failed > 0:
        print_error(f"Failed:   {failed}")


def check_port(host, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except Exception:
        return False


def port_check():
    host = input("\033[97m  Enter hostname or IP: \033[0m").strip()
    if not host:
        print_error("No host entered.")
        return

    ports_input = input("\033[97m  Enter ports (comma-separated, e.g. 80,443,22): \033[0m").strip()
    if not ports_input:
        print_error("No ports entered.")
        return

    try:
        ports = [int(p.strip()) for p in ports_input.split(",")]
    except ValueError:
        print_error("Invalid port number. Use comma-separated integers.")
        return

    ip = resolve_hostname(host)
    if ip:
        print_info(f"Resolved: {host} -> {ip}")
    else:
        ip = host

    print_header(f"Port Check: {host}")
    print()

    for port in ports:
        is_open = check_port(ip, port)
        if is_open:
            print_success(f"Port {port:<6} OPEN")
        else:
            print_error(f"Port {port:<6} CLOSED")


def main():
    print_banner()

    while True:
        print("\033[97m  ---- Menu ----\033[0m")
        print("    1) My Network Info")
        print("    2) Lookup Hostname -> IP")
        print("    3) Reverse Lookup IP -> Hostname")
        print("    4) Batch Lookup (from file)")
        print("    5) Port Check")
        print("    6) Quit")
        print()

        choice = input("\033[97m  Choose an option [1-6]: \033[0m").strip()

        if choice == "1":
            show_my_network_info()
            print()

        elif choice == "2":
            hostname = input("\n\033[97m  Enter hostname (e.g. google.com): \033[0m").strip()
            if hostname:
                lookup_hostname(hostname)
            else:
                print_error("No hostname entered.")
            print()

        elif choice == "3":
            ip = input("\n\033[97m  Enter IP address (e.g. 8.8.8.8): \033[0m").strip()
            if ip:
                lookup_ip(ip)
            else:
                print_error("No IP entered.")
            print()

        elif choice == "4":
            batch_lookup()
            print()

        elif choice == "5":
            port_check()
            print()

        elif choice in ("6", "q", "quit", "exit"):
            print()
            print_info("Goodbye!")
            print()
            break

        else:
            print_error("Invalid choice. Please enter 1-6.")
            print()


if __name__ == "__main__":
    main()
