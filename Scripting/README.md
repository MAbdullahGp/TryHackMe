# Scripting — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Programming-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Type](https://img.shields.io/badge/Type-UDP_Sockets_&_AES--GCM-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete writeup for the **Scripting** room on TryHackMe, highlighting network socket programming, UDP packet handling, and AES-GCM authenticated decryption.

---

## 📋 Executive Summary
The Scripting room evaluates proficiency in rapid offensive scripting across three progressively complex challenges. Task 3 requires establishing a raw UDP socket conversation on port 4000, parsing server instructions to extract a target SHA-256 integrity checksum, decrypting candidate flag packets using AES-GCM with recovered key and nonce parameters, and validating checksum integrity to extract the authentic flag.

* **Target Port:** UDP 4000
* **Core Technologies:** Raw UDP sockets, Cryptography (`hazmat.primitives.ciphers.aead.AESGCM`), SHA-256
* **Artifacts in Directory:**
  * `Task3.py`: Complete Python UDP socket and AES-GCM solver script

---

## 🔍 Stage 1: Protocol & Task Specification

### 1.1 Handshake Sequence
Connecting to the UDP service on port 4000:
1. Client transmits: `hello` -> Server responds with greeting.
2. Client transmits: `ready` -> Server provides instructions containing:
   * Decryption Key: `thisisaverysecretkeyl337`
   * Nonce / IV: `secureivl337`
   * Expected SHA-256 Checksum: Specified in hex.
3. Polling Flags: Client sends `final` repeatedly. For each iteration, the server sends two consecutive UDP datagrams:
   * Datagram 1: Ciphertext bytes
   * Datagram 2: 16-byte GCM authentication tag

Many transmitted flags are decoys with valid GCM formatting but mismatched integrity checksums.

---

## 🛠️ Stage 2: Exploit Solution (`Task3.py`)

```python
import socket
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SERVER_IP = "10.49.170.119"
SERVER_PORT = 4000

def solve():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)

    try:
        # Handshake
        sock.sendto(b"hello", (SERVER_IP, SERVER_PORT))
        print(sock.recvfrom(4096)[0].decode())

        sock.sendto(b"ready", (SERVER_IP, SERVER_PORT))
        instructions = sock.recvfrom(4096)[0]

        key = b"thisisaverysecretkeyl337"
        nonce = b"secureivl337"

        checksum_target_bytes = instructions.split(b"checksum of ")[1].split(b" send final")[0]
        checksum_hex = checksum_target_bytes.hex()
        aesgcm = AESGCM(key)

        print("[*] Polling datagrams and validating SHA256 checksums...")
        while True:
            sock.sendto(b"final", (SERVER_IP, SERVER_PORT))
            ciphertext = sock.recvfrom(4096)[0]

            sock.sendto(b"final", (SERVER_IP, SERVER_PORT))
            tag = sock.recvfrom(4096)[0]

            try:
                plaintext = aesgcm.decrypt(nonce, ciphertext + tag, None)
                if hashlib.sha256(plaintext).hexdigest() == checksum_hex:
                    print(f"\n[+] SUCCESS! Valid Flag Found: {plaintext.decode()}")
                    break
            except Exception:
                continue

    finally:
        sock.close()

if __name__ == "__main__":
    solve()
```

---

## 🛡️ Key Takeaways
1. **Authenticated Encryption (AEAD):** AES-GCM ensures both confidentiality and authenticity. Never reuse a static nonce with the same key across multiple encryption calls in production.
2. **Datagram Reliability:** Because UDP is connectionless and does not guarantee packet delivery or order, robust client scripts must handle timeouts and payload verification.
