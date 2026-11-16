# Burp Suite: Intruder & Practical Testing — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy/Medium-yellow.svg)
![Tool](https://img.shields.io/badge/Tool-Burp_Suite_Intruder-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup and reference guide for the **Burp Suite: Intruder** lab on TryHackMe, featuring credential stuffing and attack configurations against **Bastion Hosting**.

---

## 📋 Executive Summary
This lab exercises advanced usage of PortSwigger's Burp Suite Intruder. Using the simulated customer authentication portal for **Bastion Hosting** (`bastionhosting.thm`), we demonstrate the four primary Intruder attack types, fuzz authentication portals with tailored wordlists, execute credential stuffing, and analyze SSH key pairs.

* **Target Domain:** `bastionhosting.thm`
* **Artifacts in Directory:**
  * `BastionHostingCreds/`: Harvested wordlists (`usernames.txt`, `passwords.txt`, `emails.txt`, `combined.txt`)
  * `keys/`: Harvested OpenSSH private key pairs (`key1` to `key4`)

---

## ⚙️ Stage 1: Intruder Attack Modes Overview

Burp Suite Intruder supports four payload placement modes:

| Attack Type | Description | Best Used For |
| :--- | :--- | :--- |
| **Sniper** | Takes a single payload set and places each item sequentially into one target position at a time. | Fuzzing individual parameters, single-user password guessing. |
| **Battering Ram** | Takes a single payload set and places the exact same payload into all defined positions simultaneously. | Testing identical username/password combinations. |
| **Pitchfork** | Takes multiple payload sets and steps through them in lockstep (Payload 1 from Set A with Payload 1 from Set B). | Credential stuffing from pre-paired username:password dumps. |
| **Cluster Bomb** | Takes multiple payload sets and tests every possible mathematical combination (Cartesian product). | Testing a list of $N$ usernames against $M$ passwords ($N \times M$ requests). |

---

## 💥 Stage 2: Bastion Hosting Credential Stuffing

### 2.1 Attack Setup
1. Intercept a login POST request to `http://bastionhosting.thm/login`:
   ```http
   POST /login HTTP/1.1
   Host: bastionhosting.thm
   Content-Type: application/x-www-form-urlencoded

   email=§test@bastionhosting.thm§&password=§password123§
   ```
2. Set Attack Type to **Pitchfork** (or **Cluster Bomb** depending on wordlist pairing).
3. Payload Set 1: Load `BastionHostingCreds/emails.txt`
4. Payload Set 2: Load `BastionHostingCreds/passwords.txt`

### 2.2 Response Analysis & Grep Matching
* Configure **Grep - Match** on the phrase `Invalid credentials` or sort results by **HTTP Status Code** and **Content-Length**.
* Successful logins return a 302 Redirect to `/dashboard` or significantly differing response byte lengths, identifying valid account pairings.

---

## 🔑 Stage 3: SSH Key Analysis (`keys/`)

The directory houses four extracted OpenSSH private keys:
```bash
chmod 600 keys/key*
```
Testing the recovered user credentials against SSH access using the private keys:
```bash
ssh -i keys/key1 user@bastionhosting.thm
```
Inspecting keys and headers reveals unencrypted Ed25519 and RSA keys granting terminal access into the Bastion Hosting infrastructure.

---

## 🛡️ Remediation
1. **Enforce Multi-Factor Authentication (MFA):** Neutralize credential stuffing attacks by requiring one-time time-based tokens (TOTP).
2. **Account Lockout & Rate-Limiting:** Implement automated throttling and progressive delays on failed login attempts.
3. **Monitor Credential Stuffing:** Integrate threat intelligence feeds to detect previously leaked or compromised corporate passwords.
