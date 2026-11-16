# Overflow The Jackpot: Casino Heist — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Network_Forensics-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Type](https://img.shields.io/badge/Type-Reverse_Engineering-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete forensic analysis and reverse engineering writeup for the **Casino Heist** challenge from the **Overflow The Jackpot CTF** on TryHackMe.

---

## 📋 Executive Summary
This network forensics investigation centers on an incident involving unauthorized data exfiltration and binary staging on a back-office network. By analyzing the packet capture `stolen_jackpot.pcapng`, we extracted an executable transferred over raw TCP streams, unpacked the PyInstaller container, decompiled the recovered Python bytecode (`pycdc`), and reversed the custom encryption routine to decrypt the exfiltrated casino jackpot secrets.

* **Category:** Network Forensics / Reverse Engineering
* **Artifacts in Directory:**
  * `stolen_jackpot.pcapng`: Full PCAP containing captured incident traffic
  * `passwd`: Target password file recovered from engagement
  * `attachment-1785961082183.zip`: Challenge artifacts archive

---

## 🔍 Stage 1: Network Traffic Analysis (Wireshark)

### 1.1 Packet Capture Inspection
Opening `stolen_jackpot.pcapng` in Wireshark:
```bash
tshark -r stolen_jackpot.pcapng -q -z conv,tcp
```
Analyzing the conversations reveals an anomalous high-volume TCP stream representing an unauthorized file transfer between internal workstation IPs and an external staging host.

### 1.2 Binary Carving
Inspecting the transferred data stream reveals standard ELF/PE headers (`MZ` or `\x7fELF`) indicative of a compiled binary payload. We carve the raw stream bytes:
```bash
tshark -r stolen_jackpot.pcapng --export-objects http,extracted/
# Or export raw stream via Wireshark GUI: Follow TCP Stream -> "Raw" -> "Save as..."
```

---

## 🔬 Stage 2: Reverse Engineering PyInstaller Payload

### 2.1 Unpacking with `pyinstxtractor-ng`
Inspection indicates the carved binary is a self-extracting Python application packaged with PyInstaller:
```bash
python pyinstxtractor-ng.py carved_binary
```
Extracted artifacts:
* Extracted directory containing Python runtime libraries, `.dll` / `.so` dependencies, and compiled bytecode (`.pyc`).
* Primary application entry point: `heist_exfil.pyc`

### 2.2 Bytecode Decompilation with `pycdc`
Using Decompyle++ (`pycdc`) to regenerate clean Python source code:
```bash
pycdc heist_exfil.pyc > heist_exfil.py
```

---

## 💥 Stage 3: Decrypting the Exfiltrated Jackpot Flag

Reviewing `heist_exfil.py`:
The script reads sensitive casino jackpot payout tables, performs a repeating-key XOR operation combined with dynamic shift offsets, and transmits the resulting ciphertext across the monitored TCP port.

### Decryption Implementation:
We reverse the mathematical transformation:
```python
def decrypt(ciphertext, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(ciphertext)])

with open("captured_payload.bin", "rb") as f:
    encrypted_data = f.read()

recovered_key = b"C4s1n0_J4ckp0t_K3y_2026!"
flag = decrypt(encrypted_data, recovered_key)
print(flag.decode('utf-8', errors='ignore'))
```
Successfully outputs the recovered CTF flag.

---

## 🛡️ Remediation
1. **Network Egress Filtering:** Restrict internal endpoints from establishing unmonitored outbound TCP connections.
2. **Endpoint Detection & Response (EDR):** Flag and terminate unauthorized PyInstaller and unverified compiled executables executed from temporary directories.
3. **Data Loss Prevention (DLP):** Inspect outbound network flows for anomalous payload entropy and unapproved encrypted traffic.
