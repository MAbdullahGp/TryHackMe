# Cypher — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Cryptography-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![Type](https://img.shields.io/badge/Type-Progressive_Caesar-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A concise cryptographic challenge writeup for the **Cypher** room on TryHackMe, solving an index-shifted progressive Caesar cipher.

---

## 📋 Executive Summary
The Cypher challenge provides an encrypted string stored in `message.txt`. Analysis indicates that the encryption algorithm is a variation of the Caesar cipher where each character's shift value increments dynamically based on its 0-indexed position within the ciphertext.

* **Category:** Cryptography
* **Decoded Flag:** `a_sm4ll_crypt0_message_to_st4rt_with_THM_cracks`
* **Artifacts in Directory:**
  * `message.txt`: Encrypted ciphertext string
  * `script.py`: Custom Python decryption script

---

## 🔍 Stage 1: Cipher Analysis

### 1.1 Encrypted Ciphertext
Inspecting `message.txt`:
```text
a_up4qr_kaiaf0_bujktaz_qm_su4ux_cpbq_ETZ_rhrudm
```

### 1.2 Algorithm Reversal
Notice that:
* Non-alphabetic characters (digits and underscores) are preserved without shifting.
* The first character `a` remains `a` (shift offset 0).
* Alphabetic characters are shifted forward during encryption by index $i$:
  $$C_i = (P_i + i) \pmod{26}$$
* To decrypt, we subtract the index $i$ from each character's alphabetical position:
  $$P_i = (C_i - i) \pmod{26}$$

---

## 🛠️ Stage 2: Decryption Script (`script.py`)

```python
with open("message.txt", "r") as f:
    ciphertext = f.read().strip()

def dec(ciphertext):
    return "".join(
        chr((ord(c) - (base := ord('A') if c.isupper() else ord('a')) - i) % 26 + base)
        if c.isalpha() else c
        for i, c in enumerate(ciphertext)
    )

flag = dec(ciphertext)
print(f"Decoded Flag: {flag}")
```

### Output:
```text
Decoded Flag: a_sm4ll_crypt0_message_to_st4rt_with_THM_cracks
```

---

## 🛡️ Remediation & Cryptographic Standards
Classical shift ciphers offer zero semantic security and must never be used to protect sensitive data. Modern systems require authenticated encryption schemes such as AES-256-GCM or ChaCha20-Poly1305.
