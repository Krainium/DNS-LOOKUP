# DNS Lookup — DNS & Network Information Tool

Python CLI tool for looking up DNS records, resolving hostnames, performing reverse lookups, batch resolving from files, and checking open ports. Zero external dependencies beyond `pyfiglet` — uses only Python's built-in `socket` module.

---

## What It Does

Simple, self-contained command-line utility for quick DNS and network diagnostics without needing heavy tools like `nslookup`, `dig`, or `nmap`. Resolve domains, check what hostname an IP belongs to, scan ports, or bulk-resolve a list of hosts — all from one interactive menu.

---

## Features

- Local network info — view your hostname, FQDN, DNS IP, local IP, and all network addresses
- Hostname lookup — resolve any domain to its IPv4 and IPv6 addresses
- Reverse DNS — look up the hostname behind any IP with forward/reverse match verification
- Batch lookup — resolve an entire file of hostnames at once in a formatted table
- Port checking — check if specific ports are open on any host
- Zero heavy dependencies — only `pyfiglet` needed, everything else is Python built-in
- Windows, macOS, Linux

---

## Requirements

- Python 3.7+
- One pip package:

```bash
pip install pyfiglet
```

---

## Quick Start

```bash
pip install pyfiglet
python dns-lookup.py
```

---

## Menu

```
  ---- Menu ----
    1) My Network Info
    2) Lookup Hostname -> IP
    3) Reverse Lookup IP -> Hostname
    4) Batch Lookup (from file)
    5) Port Check
    6) Quit
```

---

## Usage

### 1) My Network Info

Displays your machine's network details — hostname, FQDN, DNS IP, local IP, all addresses, and reverse DNS.

```
  [Your Network Information]

  [*] Hostname:    DESKTOP-ABC123
  [*] FQDN:        DESKTOP-ABC123.local
  [+] DNS IP:      192.168.1.105
  [+] Local IP:    192.168.1.105

  [*] All addresses:
    IPv4  192.168.1.105
    IPv6  fe80::1a2b:3c4d:5e6f:7890

  [*] Reverse DNS: DESKTOP-ABC123
```

### 2) Lookup Hostname → IP

Resolve any domain to its IP addresses with reverse DNS verification:

```
  Enter hostname: github.com

  [+] Resolved:   github.com -> 140.82.121.4
  [*] Reverse DNS: lb-140-82-121-4-iad.github.com
```

### 3) Reverse Lookup IP → Hostname

Find the hostname behind any IP. Automatically verifies forward/reverse DNS match:

```
  Enter IP: 8.8.8.8

  [+] Resolved:  8.8.8.8 -> dns.google
  [*] Forward:   dns.google -> 8.8.8.8
  [+] Forward and reverse DNS match
```

When they don't match:
```
  [!] Forward and reverse DNS do NOT match
```

### 4) Batch Lookup (from file)

Resolve a list of hostnames from a text file, one per line. Lines starting with `#` are skipped:

```
  Enter file path: hosts.txt

  Hostname                    IP Address         Status
  ─────────────────────────── ────────────────── ───────
  google.com                  142.250.80.46      OK
  github.com                  140.82.121.4       OK
  example.com                 93.184.216.34      OK
  fake.invalid                -                  FAIL
  stackoverflow.com           151.101.1.69       OK

  [+] Resolved: 4
  [-] Failed:   1
```

### 5) Port Check

Check if specific ports are open on any host:

```
  Enter hostname or IP: google.com
  Enter ports: 80,443,22,3306

  [+] Port 80     OPEN
  [+] Port 443    OPEN
  [-] Port 22     CLOSED
  [-] Port 3306   CLOSED
```

---

## Common Use Cases

| Task | Option | Example |
|------|--------|---------|
| Check your own IP | 1 | See DNS IP and Local IP |
| Find a website's IP | 2 | `google.com` → `142.250.80.46` |
| Identify who owns an IP | 3 | `8.8.8.8` → `dns.google` |
| Resolve a list of domains | 4 | Point to a `.txt` file |
| Check if a server port is open | 5 | `myserver.com` ports `80,443,22` |
| Verify DNS propagation | 2 | Look up your domain after DNS changes |
| Verify email server PTR records | 3 | Check forward/reverse DNS match |

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing pyfiglet | Not installed | `pip install pyfiglet` |
| Could not resolve hostname | Typo or including `https://` in input | Use just the domain — e.g. `google.com` |
| All ports show CLOSED | Firewall or slow host | Try a known-open port like `443` on `google.com` |
| Batch file not found | Wrong path | Use the full file path |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `pyfiglet` | ASCII art banner |

All DNS resolution and port checking uses Python's built-in `socket` module.
