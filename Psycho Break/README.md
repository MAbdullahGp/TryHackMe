# Psycho Break — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Boot2Root-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy/Medium-yellow.svg)
![OS](https://img.shields.io/badge/OS-Linux-success.svg)
![Theme](https://img.shields.io/badge/Theme-The_Evil_Within-purple.svg)

A complete penetration testing writeup for the **Psycho Break** room on TryHackMe, themed around *The Evil Within*.

---

## 📋 Executive Summary
Psycho Break combines web exploration, audio Morse-code decoding, steganographic image extraction, FTP credential recovery, binary dictionary brute-forcing, and cryptographic cipher decoding.

* **Target OS:** Linux
* **Initial Access:** Steganography on `Table.jpg` -> FTP credentials for user `joseph`.
* **Privilege Escalation:** Binary brute-force using `random.dic` -> Root key decryption.
* **Artifacts in Directory:**
  * `brute.py`: Python dictionary attack automation script
  * `random.dic`: Targeted dictionary file
  * `program`: Compiled ELF executable
  * `helpme.zip`: Recovered challenge archive

---

## 🔍 Stage 1: Reconnaissance & Steganography

### 1.1 Web Exploration & Audio Clue
* Exploring the web portal reveals an audio Morse-code track.
* Decoding the Morse code produces the passphrase:
  ```text
  SHOWME
  ```

### 1.2 Steganography on `Table.jpg`
Extracting `helpme.zip` yields a note from Joseph and an image file `Table.jpg`.
Using `steghide` with the decoded passphrase `SHOWME`:
```bash
steghide extract -sf Table.jpg -p SHOWME
```
Extracted credentials:
```text
user: joseph
pass: intotheterror445
```

---

## 💥 Stage 2: Initial Foothold (FTP to Binary Retrieval)

### 2.1 FTP Access
Logging in to FTP with Joseph's credentials:
```bash
ftp <TARGET_IP>
Name: joseph
Password: intotheterror445
```
Downloaded challenge files:
* `program` (compiled 64-bit ELF executable)
* `random.dic` (wordlist)

---

## 📈 Stage 3: Binary Brute-Forcing & Decryption

### 3.1 Automating the Dictionary Attack (`brute.py`)
The `program` binary takes a password argument from `random.dic`. We scripted the brute-force attack in `brute.py`:
```python
import subprocess

with open("random.dic", "r") as f:
    for line in f:
        key = line.strip()
        if not key:
            continue
        result = subprocess.run(["./program", key], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[+] Found correct password: {key}")
            print(f"[+] Output: {result.stdout.strip()}")
            break
```
Running `brute.py`:
```text
[+] Found correct password: kidman
[+] Output: Successfully authenticated! Decryption key and flag fragments revealed...
```

### 3.2 Decoding the Ciphertext
The binary output provides an encoded cipher string. Decoding via CyberChef yields root credentials and the final room flag.

---

## 🛡️ Remediation
1. Avoid relying on security-through-obscurity via steganography.
2. Enforce strong password hashing and eliminate small dictionary keys in custom authentication binaries.
