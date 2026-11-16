# CyberChef: The Cyber Swiss Army Knife & Offline Suite

![Category](https://img.shields.io/badge/Category-Offensive_Tooling-blue.svg)
![Tool](https://img.shields.io/badge/Tool-CyberChef-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Browser_Offline-brightgreen.svg)

A complete guide and offline installation bundle for GCHQ's **CyberChef**, the definitive web application for data decoding, cryptographic analysis, deobfuscation, and file extraction.

---

## 📋 Executive Summary
CyberChef enables rapid analysis and manipulation of data formats without requiring ad-hoc terminal scripting. This directory hosts an offline, standalone build of CyberChef (`CyberChef_a1c2df029ecb5477305a3af1161df6de56d8612a`), ensuring researchers can analyze sensitive payloads and forensic artifacts in isolated, air-gapped environments.

* **Artifacts in Directory:**
  * `CyberChef_*.zip`: Offline standalone distribution archive
  * `CyberChef_*/`: Unpacked HTML/JavaScript bundle ready for offline execution

---

## 🚀 Running Offline CyberChef

To launch CyberChef locally without internet access:
```bash
# Option 1: Open index.html directly in a browser
firefox cybercheff/CyberChef_*/index.html &

# Option 2: Serve via local Python HTTP server
cd cybercheff/CyberChef_*
python3 -m http.server 8000
# Navigate to http://localhost:8000
```

---

## 🧪 Top 10 Essential CTF Recipes

| Recipe Operation | Purpose |
| :--- | :--- |
| **Magic** | Automatically analyzes input byte entropy and suggests matching decodings and file extractions. |
| **From Base64** | Decodes standard and URL-safe Base64 encoded strings. |
| **From Hex** | Converts hexadecimal strings into raw ASCII/binary output. |
| **URL Decode** | Decodes percent-encoded HTTP parameters and query strings. |
| **XOR** | Performs dynamic single-byte or multi-byte XOR decryption. |
| **Gunzip / Uncompress** | Decompresses gzip-compressed payloads extracted from network streams. |
| **JWT Decode** | Decodes and pretty-prints JSON Web Token headers and claims. |
| **Extract URLs / IP addresses** | Uses regex pipelines to parse indicators of compromise (IoCs) from raw text. |
| **Render Image** | Renders carved raw binary bytes into PNG, JPEG, or GIF graphics. |
| **Entropy** | Visualizes Shannon entropy to differentiate between plaintext, encrypted, and compressed data blocks. |
