# Checkmate — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-CTF-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration test walkthrough for the **Checkmate** room on TryHackMe, assessing weak password hygiene, default configurations, OSINT, and password-pattern cracking across multiple internal services.

---

## 📋 Executive Summary
Checkmate demonstrates how weak password policies and predictable administrative habits compromise an organization across five escalating tiers of difficulty. The target environment represents services managed by administrator **Marco Bianchi**.

* **Target OS:** Linux
* **Artifacts in Directory:**
  * `marco.txt`: Level 3 recovered password (`Bianchi2495`)
  * `hash.txt`: Level 4 recovered SHA256 image upload hash
  * `security.txt`: Targeted pattern dictionary (`Security2000!` through `Security2030!`)

---

## 🔍 Stage-by-Stage Walkthrough

### 🗺️ Setup: Domain Resolution
Map the target IP address in `/etc/hosts`:
```text
<TARGET_IP> firewall.thm jobs.thm social.thm
```

---

### ♟️ Level 1: Default Credentials (Port 5001)
* **Target:** `http://firewall.thm:5001`
* **Vulnerability:** Unchanged vendor default credentials.
* **Finding:** Navigating to the firewall login portal and attempting common default passwords:
  * **Username:** `admin`
  * **Password:** `12345`

---

### ♟️ Level 2: Weak Corporate Keyword Passwords (Port 5002)
* **Target:** `http://jobs.thm:5002`
* **Vulnerability:** Reused corporate buzzwords from the landing page.
* **Methodology:** Scraping website keywords using `cewl`:
  ```bash
  cewl http://jobs.thm:5002 -w keywords.txt
  ```
  Testing extracted keywords against the portal login:
  * **Password Found:** `excellence`

---

### ♟️ Level 3: OSINT-Based Password Profiling (Port 5003)
* **Target:** `http://social.thm:5003`
* **Vulnerability:** Password constructed from publicly available personal information.
* **Methodology:** Profiling Marco Bianchi's social media page revealed personal details (surname and year of graduation/birth).
* **Password Found (`marco.txt`):** `Bianchi2495`

---

### ♟️ Level 4: SHA-256 Hash Reversal / Upload Recovery
* **Target:** Social platform profile picture.
* **Vulnerability:** The platform renames uploaded images using the raw SHA-256 hash of the original filename (`<hash>.png`).
* **Hash Recorded in `hash.txt`:**
  ```text
  d34a569ab7aaa54dacd715ae64953455d86b768846cd0085ef4e9e7471489b7b
  ```
* **Cracking with John the Ripper:**
  ```bash
  john --format=raw-sha256 --incremental=alpha hash.txt
  ```
* **Plaintext Recovered:** `family`

---

### ♟️ Level 5: Pattern-Based SSH Brute-Forcing
* **Target:** OpenSSH daemon (`<TARGET_IP>:22`)
* **Vulnerability:** Predictable password pattern combining a base keyword, year, and special character.
* **Pattern Discovered:** `Security<YEAR>!` (Years 2000 to 2030).
* **Wordlist Generation (`security.txt`):**
  Generated via Python / Crunch (`Security2000!` through `Security2030!`).
* **Hydra SSH Attack:**
  ```bash
  hydra -l marco -P security.txt <TARGET_IP> ssh
  ```
  Logging into SSH provides the final room flag.

---

## 🛡️ Remediation
1. Enforce strict minimum password complexity policies and multi-factor authentication (MFA).
2. Prohibit using predictable formulas or personal OSINT details in credentials.
3. Disable default administrator credentials upon initial system deployment.
