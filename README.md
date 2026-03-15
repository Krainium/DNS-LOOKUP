# DNS Lookup — DNS & Network Information Tool

A Python CLI tool for looking up DNS records, resolving hostnames, performing reverse lookups, batch resolving from files, and checking open ports. Zero external dependencies beyond `pyfiglet` — uses only Python's built-in `socket` module.

Created by **Krainium**.

---

## Aim

To provide a simple, self-contained command-line utility for quick DNS and network diagnostics without needing to install heavy tools like `nslookup`, `dig`, or `nmap`. Whether you need to resolve a domain, check what hostname an IP belongs to, scan ports, or bulk-resolve a list of hosts, this single script handles it all from one interactive menu.

---

## Features

- **Local network info** — view your hostname, FQDN, DNS IP, local IP, and all network addresses
- **Hostname lookup** — resolve any domain to its IPv4 and IPv6 addresses
- **Reverse DNS** — look up the hostname behind any IP address with forward/reverse match verification
- **Batch lookup** — resolve an entire file of hostnames at once in a formatted table
- **Port checking** — check if specific ports are open on any host
- **Styled output** — pyfiglet ASCII banner with color-coded results
- **Zero heavy dependencies** — only `pyfiglet` needed, everything else is Python built-in
- **Works on Windows, macOS, and Linux**

---

## Preview

```
    ____  _   _______    __                __             
   / __ \/ | / / ___/   / /   ____  ____  / /____  ______ 
  / / / /  |/ /\__ \   / /   / __ \/ __ \/ //_/ / / / __ \
 / /_/ / /|  /___/ /  / /___/ /_/ / /_/ / ,< / /_/ / /_/ /
/_____/_/ |_//____/  /_____/\____/\____/_/|_|\__,_/ .___/ 
                                                 /_/      

  DNS & Network Information Tool
  Look up DNS records, resolve hostnames,
  and view your network details.

  ─────────────────────────────────────────────

  ---- Menu ----
    1) My Network Info
    2) Lookup Hostname -> IP
    3) Reverse Lookup IP -> Hostname
    4) Batch Lookup (from file)
    5) Port Check
    6) Quit
```

---

## Requirements

- **Python 3.7+** — [Download here](https://www.python.org/downloads/)
- One pip package:

```bash
pip install pyfiglet
```

No other dependencies. All DNS and network operations use Python's built-in `socket` module.

---

## Quick Start

```bash
pip install pyfiglet
python dns-lookup.py
```

---

## Usage

### 1) My Network Info

Displays your machine's network details:

```
  [Your Network Information]

  [*] Hostname:       DESKTOP-ABC123
  [*] FQDN:           DESKTOP-ABC123.local
  [+] DNS IP:         192.168.1.105
  [+] Local IP:       192.168.1.105

  [*] All addresses for this host:
    IPv4  192.168.1.105
    IPv6  fe80::1a2b:3c4d:5e6f:7890

  [*] Reverse DNS:    DESKTOP-ABC123
```

### 2) Lookup Hostname -> IP

Resolve any domain name to its IP addresses:

```
  Enter hostname (e.g. google.com): github.com

  [Lookup: github.com]

  [+] Resolved:  github.com -> 140.82.121.4

  [*] All addresses:
    IPv4  140.82.121.4
  [*] Reverse DNS:   lb-140-82-121-4-iad.github.com
```

### 3) Reverse Lookup IP -> Hostname

Find the hostname behind any IP address:

```
  Enter IP address (e.g. 8.8.8.8): 8.8.8.8

  [Reverse Lookup: 8.8.8.8]

  [+] Resolved:  8.8.8.8 -> dns.google
  [*] Forward:   dns.google -> 8.8.8.8
  [+] Forward and reverse DNS match
```

When forward and reverse DNS don't match, the tool flags it:

```
  [!] Forward and reverse DNS do NOT match
```

### 4) Batch Lookup (from file)

Resolve a list of hostnames from a text file (one per line):

```
  Enter path to file (one hostname per line): hosts.txt

  [Batch Lookup (5 entries)]

  Hostname                                 IP Address         Status
  ──────────────────────────────────────── ────────────────── ────────
  google.com                               142.250.80.46      OK
  github.com                               140.82.121.4       OK
  example.com                              93.184.216.34      OK
  fake.invalid                             -                  FAIL
  stackoverflow.com                        151.101.1.69       OK

  [+] Resolved: 4
  [-] Failed:   1
```

**Input file format** — one hostname per line:
```
google.com
github.com
example.com
stackoverflow.com
```

Lines starting with `#` are treated as comments and skipped.

### 5) Port Check

Check if specific ports are open on any host:

```
  Enter hostname or IP: google.com
  Enter ports (comma-separated, e.g. 80,443,22): 80,443,22,3306

  [*] Resolved: google.com -> 142.250.80.46

  [Port Check: google.com]

  [+] Port 80     OPEN
  [+] Port 443    OPEN
  [-] Port 22     CLOSED
  [-] Port 3306   CLOSED
```

### 6) Quit

Exit the program.

---

## Common Use Cases

| Task | Menu Option | Example |
|------|-------------|---------|
| Check your own IP address | 1 | See DNS IP and Local IP |
| Find a website's IP | 2 | `google.com` -> `142.250.80.46` |
| Identify who owns an IP | 3 | `8.8.8.8` -> `dns.google` |
| Resolve a list of domains | 4 | Point to a `.txt` file |
| Check if a server port is open | 5 | `myserver.com` ports `80,443,22` |
| Verify DNS propagation | 2 | Look up your domain after DNS changes |
| Check forward/reverse DNS match | 3 | Verify email server PTR records |

---

## Troubleshooting

### "Missing required package: pyfiglet"

```bash
pip install pyfiglet
```

If you have both Python 2 and 3:
```bash
pip3 install pyfiglet
```

### "Could not resolve" on hostname lookup

- Check that the hostname is spelled correctly
- Make sure you're not including `http://` or `https://` — just the domain (e.g. `google.com`, not `https://google.com`)
- Check your internet connection

### Port check shows everything as CLOSED

- The host may have a firewall blocking connections
- You may need to run the script with administrator/root privileges for some port scans
- The default timeout is 3 seconds — very slow or distant hosts may not respond in time

### Batch lookup file not found

- Use the full path to the file (e.g. `C:\Users\you\hosts.txt` on Windows or `/home/you/hosts.txt` on Linux)
- Make sure the file exists and you have read permission

---

## Dependencies

| Package | Purpose |
|---------|---------|
| [pyfiglet](https://pypi.org/project/pyfiglet/) | ASCII art banner |

All DNS resolution and port checking uses Python's built-in `socket` module.
