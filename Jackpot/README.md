# Jackpot — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Binary_Exploitation-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Type](https://img.shields.io/badge/Type-Hardware_Simulation-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup for the **Jackpot** room on TryHackMe, simulating an ATM Jackpotting attack over custom XFS hardware bridges.

---

## 📋 Executive Summary
Jackpot challenges security researchers to perform an unauthorized cash-out (ATM Jackpotting) against an automated teller terminal. The environment consists of an administrative web console on port 8080 and a binary XFS bridge on port 9100. By reversing the technician's binary (`jackpot`), interacting with the custom binary protocol, computing dynamic supervisor activation tokens, and disarming safety fraud controls, all cash cassettes are emptied to unlock the flag.

* **Target Ports:**
  * Port 8080: Branch Engineering Console
  * Port 9100: XFS Hardware Bridge
* **Artifacts in Directory:**
  * `jackpot`: Discovered 64-bit ELF supervisory utility binary
  * `script.py`: Custom Python socket client automating the jackpotting sequence
  * `temp.js`: Extracted client dashboard telemetry script

---

## 🔍 Stage 1: Protocol & Service Analysis

### 1.1 Web Console (Port 8080)
Visiting `http://<TARGET_IP>:8080` displays the Branch Engineering Console showing real-time cassette statuses (bill counts in `CST1`, `CST2`), session state, a link to the diagnostic tool `jackpot`, and an active session `nonce`.

### 1.2 Binary Protocol Structure (Port 9100)
Communicating with the service on port 9100 requires custom binary framing:
* **Request Packet Structure:**
  `[1-byte msg_type] + [4-byte big-endian cmd_id] + [2-byte big-endian data_len] + [data_payload]`
* **Message Types:**
  * `0x01` (`GETINFO`): Queries hardware status, cassette balances, or requests the flag (`0x4ff`).
  * `0x02` (`EXECUTE`): Dispatches actions (Arming, disabling fraud controls, dispensing bills).
* **Response Packet Structure:**
  `[2-byte big-endian reply_len] + [JSON utf-8 payload]`

---

## 💥 Stage 2: Binary Reversal & Activation Code Generation

Running strings and decompiling the local ELF binary `jackpot`:
```bash
file jackpot
# ELF 64-bit LSB executable, x86-64
./jackpot <nonce>
```
The binary processes the dynamic session nonce issued by the XFS bridge and calculates the one-time supervisor activation code required by command `0x04f0`.

---

## 🛠️ Stage 3: Exploitation Workflow (`script.py`)

The automated exploit client `script.py` executes the full ATM jackpot sequence:

1. **Connect & Read Banner:** Establishes TCP connection to port 9100.
2. **Query Session Nonce:** Sends `GETINFO` (`0x01`) with command `0x0301`.
3. **Derive Supervisor Code:** Invokes `./jackpot <nonce>` via `subprocess` to obtain the code.
4. **Arm Supervisor Mode:** Sends `EXECUTE` (`0x02`) command `0x04f0` with the activation code.
5. **Disable Fraud Monitor:** Sends `EXECUTE` command `0x04f1` with payload `"off"`.
6. **Dispense All Bills:** Loops `EXECUTE` command `0x0401` with `{"cassette": "CST1", "count": 40}` and `{"cassette": "CST2", "count": 40}` until all cassettes reach a balance of 0.
7. **Extract Flag:** Sends `GETINFO` command `0x04ff` to pull the final challenge flag.

---

## 🛡️ Remediation
1. **Network Segmentation:** Never expose ATM physical hardware control interfaces (XFS bridges) or supervisory consoles across routable or shared network subnets.
2. **Mutual TLS (mTLS) & Hardware Authentication:** Enforce strict cryptographic mutual authentication between ATM host software and physical dispensing peripherals.
3. **Firmware Integrity & Anti-Jackpotting Defenses:** Enforce signed firmware updates and lock down physical access ports against unauthorized diagnostic tool execution.
