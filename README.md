# 🛡️ TryHackMe & Cybersecurity CTF Portfolio

[![Platform: TryHackMe](https://img.shields.io/badge/Platform-TryHackMe-red.svg?logo=tryhackme)](https://tryhackme.com)
[![Platform: PortSwigger](https://img.shields.io/badge/Platform-PortSwigger_Academy-orange.svg)](https://portswigger.net/web-security)
[![Platform: PicoCTF](https://img.shields.io/badge/Platform-PicoCTF-blue.svg)](https://play.picoctf.org)
[![Tools: Python](https://img.shields.io/badge/Language-Python_3-brightgreen.svg?logo=python)](https://python.org)
[![Security: Penetration Testing](https://img.shields.io/badge/Domain-Penetration_Testing-blueviolet.svg)](#)

A structured, comprehensive repository of penetration testing writeups, CTF challenge walk-throughs, custom exploit automation scripts, and offensive security cheatsheets. Every challenge folder features a dedicated, self-contained `README.md` documenting reconnaissance, vulnerability analysis, proof-of-concept exploitation, privilege escalation, and remediation strategies.

---

## 📑 Repository Structure & Index

### 🎯 1. Boot2Root & CTF Challenge Machines
Hands-on machine compromises spanning full attack lifecycles from reconnaissance to root.

| Machine / Challenge | Difficulty | Primary Attack Vector | Privilege Escalation | Writeup Link |
| :--- | :--- | :--- | :--- | :--- |
| **Mr. Robot** | Medium | WordPress enumeration & Hydra brute-force | SUID Nmap interactive mode | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/MrRobot/README.md) |
| **RootMe** | Easy | Insecure file upload extension bypass (`.phtml`) | SUID Python GTFOBins | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/RootMe/README.md) |
| **Simple CTF** | Easy | CMS Made Simple SQLi (CVE-2019-9053) | Sudo NOPASSWD on `/usr/bin/vim` | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/SimpleCTF/README.md) |
| **Startup** | Easy | Anonymous FTP webshell upload | Incident PCAP analysis & cron script hijack | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Startup/README.md) |
| **Vulnversity** | Easy | Extension fuzzing & upload bypass (`.phtml`) | SUID `/bin/systemctl` custom unit | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/vulnversity/README.md) |
| **Beach Bar** | Easy | Demo credential leakage & PyYAML RCE | Process argument credential harvesting | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Beach_Bar/README.md) |
| **Psycho Break** | Easy/Med | Audio Morse code & Steganography | Binary dictionary attack with `random.dic` | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Psycho%20Break/README.md) |
| **Checkmate** | Easy | 5-Tier password auditing & OSINT profiling | SSH pattern brute-force with Crunch & Hydra | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Checkmate/README.md) |

---

### 🔬 2. Advanced Challenges & Specialized Labs
Reverse engineering, hardware/CAN bus simulation, protocol reversing, and cryptographic ciphers.

| Room / Challenge | Category | Core Mechanics & Concepts | Writeup Link |
| :--- | :--- | :--- | :--- |
| **Grand Larceny Auto II** | Reverse Engineering | .NET DLL decompilation, HMAC key extraction, API rate-limit bypass | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Grand%20Larceny%20Auto%20II/README.md) |
| **Jackpot** | Binary / Hardware | ATM Jackpotting simulation over XFS bridge (Port 9100), supervisor activation | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Jackpot/README.md) |
| **Casino Heist (Overflow)** | Network Forensics | Wireshark TCP stream extraction, PyInstaller unpacking, PyCDC decompilation | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/thm-ctf-jackpot-overflow/README.md) |
| **Phantom Fob** | Automotive / CAN | Socketcand TCP bridge (Port 29536), CAN ID 421 replay attack, SSE telemetry | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/PhantomFob/README.md) |
| **Prioritise** | Web / SQLi | Boolean-based blind SQL injection in `ORDER BY` clause using SQL `CASE` statements | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Prioritise/README.md) |
| **The Letter** | OSINT / Historical | Gallica BnF archives, 1925 Finistère rescue hero identification, postal barcodes | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/letter/README.md) |
| **Missing Person** | OSINT / Geolocation | Mandalika MotoGP circuit tracing, EXIF metadata extraction, local social tracing | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Missing%20Person/README.md) |
| **Moniker Link** | Vulnerability / NTLM | Outlook CVE-2024-21413 Protected View bypass via `file://` moniker, Responder | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/MonikerLink/README.md) |
| **Cypher** | Cryptography | Dynamic progressive Caesar shift cipher recovery via Python | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/cypher/README.md) |
| **Scripting** | Sockets / Cryptography | UDP socket communication (Port 4000), instructions parsing, AES-GCM decryption | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/Scripting/README.md) |

---

### 🌐 3. Web Vulnerability & Topic Labs
Dedicated modules analyzing specific web application vulnerabilities and attack vectors.

| Topic / Room | Focus Area | Key Concepts Demonstrated | Writeup Link |
| :--- | :--- | :--- | :--- |
| **Authentication Bypass** | Web Security | Verbose JSON login error enumeration & automated email checking | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/authentication/README.md) |
| **Burp Suite: Intruder** | Web Tooling | Sniper, Battering Ram, Pitchfork, and Cluster Bomb credential stuffing | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/BurpSuite/README.md) |
| **File Inclusion** | Web Security | LFI, RFI, PHP filter wrappers (`php://filter`), Apache log poisoning | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/fileinclusion/README.md) |
| **HTTP Request Smuggling** | Advanced Web | CL.TE, TE.CL, and TE.TE HTTP/1.1 pipeline desynchronization | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/http_request_smuggle/README.md) |
| **JWT Security** | Web Security | HMAC secret cracking (`jwt.secrets.list`), `none` algorithm token forgery | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/jwtsecurity/README.md) |
| **LDAP Injection** | Web Security | Blind boolean wildcard injection (`*)(|(&`) with character probing | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/ldapinjection/README.md) |
| **Password Cracking** | Cryptography | Cracking MD5, SHA-256, Windows NTLM, and UNIX bcrypt using Hashcat/John | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/password_cracking/README.md) |
| **Linux Privilege Escalation** | System Security | Ingestion pipeline exploitation in `/incoming`, `pspy64` monitoring, SSH keys | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/prvEscalation/README.md) |
| **SSRF** | Web Security | Loopback bypass, cloud instance metadata exfiltration, custom HTTP receiver | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/ssrfhr/README.md) |
| **Web Exploitation 2** | Windows / IIS | Insecure WebDAV `PUT` method, ASPX webshell execution, PowerShell reverse shell | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/webexploit2/README.md) |
| **Wordlist Room** | Offensive Tooling | Targeted website scraping with CeWL, username permutation schemas | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/WordlistRoom/README.md) |
| **PortSwigger Series** | Web Security | Apache `.htaccess` MIME mapping (`.l33t`), Server-Side Includes (SSI) injection | [View Writeup](file:///home/abdullahgp/Documents/TryHackMe/PortSwiggerSeries/README.md) |

---

### 🧰 4. Reference Cheatsheets, Tooling & External CTF
Operational references, environment stabilization guides, and tools.

| Resource | Description | Writeup Link |
| :--- | :--- | :--- |
| **Master Cheatsheet (`important/`)** | Linux SUID, `LD_PRELOAD` shared library hijacking, Windows unattended creds, TTY stabilization | [View Cheatsheet](file:///home/abdullahgp/Documents/TryHackMe/important/README.md) |
| **Tmux Cheatsheet** | Visual terminal multiplexing guide: sessions, windows, splits, and buffer navigation | [View Cheatsheet](file:///home/abdullahgp/Documents/TryHackMe/Tmux%20cheatsheat/README.md) |
| **Vim Practical Guide** | Modal editing, navigation motions, text manipulation, and regex substitution | [View Guide](file:///home/abdullahgp/Documents/TryHackMe/toolboxvim/README.md) |
| **Python Offensive Tooling** | Building custom web clients, session handling, error evaluation, and multithreading | [View Guide](file:///home/abdullahgp/Documents/TryHackMe/Python/README.md) |
| **CyberChef Offline Suite** | Standalone offline distribution and recipe cookbook for data deobfuscation and decoding | [View Guide](file:///home/abdullahgp/Documents/TryHackMe/cybercheff/README.md) |
| **PicoCTF Framework** | Challenge repository structure and methodologies across Binary, Crypto, Web, and Forensics | [View Guide](file:///home/abdullahgp/Documents/TryHackMe/PicoCTF/README.md) |

---

## 🔄 General Penetration Testing Methodology

```
+-----------------------------------------------------------------------------------+
| 1. RECONNAISSANCE & ENUMERATION                                                   |
|    * Port Scanning (Nmap: TCP/UDP, Service Versioning, OS Fingerprinting)         |
|    * Web Enumeration (Gobuster, Feroxbuster, Nikto, robots.txt, sitemap.xml)      |
|    * Source Code & Comment Inspection (HTML comments, client JS, API endpoints)  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. VULNERABILITY ANALYSIS & FOOTHOLD                                              |
|    * Web Exploitation (SQLi, LFI/RFI, Command Injection, File Upload Bypasses)   |
|    * Authentication Testing (Hydra, Burp Intruder, Verbose Error Enumeration)     |
|    * Webshell Staging & Interactive Shell Spawning (Netcat, PentestMonkey)       |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. POST-EXPLOITATION & STABILIZATION                                              |
|    * TTY Upgrades (Python pty, stty raw -echo, TERM=xterm-256color)                |
|    * Internal Reconnaissance (LinPEAS, WinPEAS, pspy64, sudo -l, SUID binaries)   |
|    * Credential Harvesting (/etc/shadow, KeePass, config files, bash history)     |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. PRIVILEGE ESCALATION TO ROOT / SYSTEM                                          |
|    * SUID / SGID Binary Abuse (GTFOBins)                                          |
|    * Insecure Cronjobs & Automated Pipelines (Writable scripts, PATH hijacking)   |
|    * Sudo Rights & Shared Library Hijacking (LD_PRELOAD)                          |
|    * Windows Service Exploitation (Unquoted service paths, AlwaysInstallElevated) |
+-----------------------------------------------------------------------------------+
```

---

## ⚖️ Legal Disclaimer
All tools, scripts, and documentation within this repository were created strictly for educational purposes and authorized penetration testing within controlled lab environments (such as TryHackMe, PortSwigger Web Security Academy, and PicoCTF). Unauthorized access to computer systems without explicit written consent is illegal.
