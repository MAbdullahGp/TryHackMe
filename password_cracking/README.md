# Password Cracking & Cryptographic Hashes — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Cryptography-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy/Medium-yellow.svg)
![Tools](https://img.shields.io/badge/Tools-Hashcat_&_John-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete reference writeup and practical lab guide for **Password Cracking** on TryHackMe, covering hash identification, cracking methodologies with Hashcat and John the Ripper, and salt handling across MD5, SHA-256, NTLM, and bcrypt.

---

## 📋 Executive Summary
Password cracking is an essential post-exploitation and auditing discipline. This room explores the identification and cracking of four foundational hash types recovered from system breaches and web databases: MD5, SHA-256, Windows NTLM, and UNIX bcrypt.

* **Tools Utilized:** Hashcat, John the Ripper, `hashid`, `rockyou.txt`
* **Artifacts in Directory:**
  * `hash1.txt` / `demo.txt`: MD5 hashes
  * `hash2.txt`: SHA-256 hash
  * `hash3.txt` / `demo2.txt` / `demo3.txt`: Windows NTLM hashes
  * `hash4.txt`: Modular bcrypt hash (`$2b$05$...`)

---

## 🔍 Stage 1: Hash Identification & Profiling

Using `hash-identifier` or `hashid`:
```bash
hashid -m hash1.txt
```

| File | Hash Sample / Format | Identified Algorithm | Hashcat Mode | John Format |
| :--- | :--- | :--- | :--- | :--- |
| `hash1.txt` | `e10adc3949ba59abbe56e057f20f883e` (32 hex) | **MD5** | `-m 0` | `raw-md5` |
| `hash2.txt` | `5e884898da28047151d0e56f8dc62927...` (64 hex) | **SHA-256** | `-m 1400` | `raw-sha256` |
| `hash3.txt` | `8846f7eaee8fb117ad06bdd830b7586c` (32 hex) | **NTLM** | `-m 1000` | `nt` |
| `hash4.txt` | `$2b$05$9I7YCSrgm6aLO7J5YPC9x.Kp...` (Modular) | **bcrypt** | `-m 3200` | `bcrypt` |

---

## 💥 Stage 2: Cracking Walkthrough

### 2.1 MD5 (`hash1.txt`)
```bash
# Hashcat
hashcat -m 0 hash1.txt /usr/share/wordlists/rockyou.txt
# Plaintext: 123456
```

### 2.2 SHA-256 (`hash2.txt`)
```bash
# Hashcat
hashcat -m 1400 hash2.txt /usr/share/wordlists/rockyou.txt
# Plaintext: password
```

### 2.3 Windows NTLM (`hash3.txt`)
```bash
# Hashcat
hashcat -m 1000 hash3.txt /usr/share/wordlists/rockyou.txt
# Or John the Ripper:
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt hash3.txt
```

### 2.4 Bcrypt (`hash4.txt`)
Bcrypt features a salt and adjustable cost factor (`$2b$05$`), designed to be computationally intensive to resist GPU hardware brute-forcing:
```bash
# Hashcat
hashcat -m 3200 hash4.txt /usr/share/wordlists/rockyou.txt
# John the Ripper
john --format=bcrypt --wordlist=/usr/share/wordlists/rockyou.txt hash4.txt
```

---

## 🛡️ Remediation & Storage Recommendations
1. **Never Use Unsalted or Fast Hashes:** MD5, SHA-1, and standard SHA-256 can be computed at billions of hashes per second on consumer GPUs.
2. **Adopt Modern Memory-Hard KDFs:** Use **Argon2id** (winner of the Password Hashing Competition) or **bcrypt** with a minimum cost factor of 12.
3. **Unique Cryptographic Salting:** Ensure a cryptographically secure random salt (minimum 16 bytes) is generated per user credential.
