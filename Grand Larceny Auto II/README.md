# Grand Larceny Auto II — TryHackMe Writeup

![Category](https://img.shields.io/badge/Category-Game_Hacking-blue.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange.svg)
![Type](https://img.shields.io/badge/Type-Reverse_Engineering-purple.svg)
![Platform](https://img.shields.io/badge/Platform-TryHackMe-red.svg)

A comprehensive, technical writeup for the **Grand Larceny Auto II** room on TryHackMe, focusing on .NET game assembly decompilation, client-side HMAC signature forgery, rate-limiting evasion, and API parameter manipulation.

---

## 📋 Executive Summary
*Grand Larceny Auto II* is a game security challenge built with the Godot Engine and C#. Unlike the original room which permitted static flag discovery, this sequel introduces an authoritative backend API (`http://gla2.thm`). By decompiling `GrandLarcenyAuto.dll`, we recovered the client-side HMAC-SHA256 signing key, reversed the role derivation algorithm (`DeriveStaffRole`), bypassed anti-cheat pacing via timed requests, and manipulated the unsigned `role` parameter on the `/claim` endpoint to claim the staff flag.

* **Target URL:** `http://gla2.thm`
* **Vulnerabilities:** Hardcoded cryptographic keys in client assemblies, insecure client-side role derivation, and parameter tampering on checkout.
* **Artifacts in Directory:**
  * `script.py`: Full end-to-end Python exploitation script.

---

## 🔍 Stage 1: Reverse Engineering the Client Assembly

### 1.1 Decompiling `GrandLarcenyAuto.dll`
Using ILSpy / dnSpy on the managed game assembly `GrandLarcenyAuto.dll`, we inspect the client communication classes (`PoPClient` / `NetworkManager`):

1. **Hardcoded HMAC Key:**
   ```csharp
   private static readonly byte[] SIGN_KEY = Encoding.UTF8.GetBytes("gla2_crew_sign_v1_2f9b6c8ad14e");
   ```
   The client calculates HMAC-SHA256 signatures over state transitions:
   $$\text{sig} = \text{HMAC-SHA256}(\text{SIGN\_KEY}, \text{session\_id} + "|" + \text{step} + "|" + \text{token})$$

2. **Staff Role Derivation Logic (`DeriveStaffRole`):**
   ```csharp
   public static string DeriveStaffRole(List<int> stashOrder) {
       string input = $"heat5_stash{stashOrder[0]}_stash{stashOrder[1]}_stash{stashOrder[2]}_vault";
       return BitConverter.ToString(SHA1.Create().ComputeHash(Encoding.UTF8.GetBytes(input))).Replace("-", "").ToLower();
   }
   ```

---

## 💥 Stage 2: Anti-Cheat & API Mechanics

The backend exposes three primary REST endpoints:
* `POST /session`: Initializes game state, issuing a `session_id`, initial `token`, and randomized `stash_order`.
* `POST /checkpoint`: Validates sequential checkpoint progression (`heat5` -> `stashA` -> `stashB` -> `stashC` -> `vault`). Requires a valid HMAC signature and enforces an anti-cheat rate limit: requests submitted faster than 6.0 seconds are rejected.
* `POST /claim`: Finalizes the heist and rewards the flag. Expects `session_id`, `role`, `token`, and `sig`. Crucially, the HMAC signature signs only `{session_id}|claim|{token}`, leaving `role` unsigned and vulnerable to tampering!

---

## 🛠️ Stage 3: Exploit Implementation (`script.py`)

We automated the entire heist progression with `script.py`:
```python
#!/usr/bin/env python3
import hashlib, hmac, time, requests

BASE_URL = "http://gla2.thm"
SIGN_KEY = b"gla2_crew_sign_v1_2f9b6c8ad14e"

def sign(data: str) -> str:
    return hmac.new(SIGN_KEY, data.encode("utf-8"), hashlib.sha256).hexdigest()

def derive_staff_role(stash_order: list) -> str:
    role_str = f"heat5_stash{stash_order[0]}_stash{stash_order[1]}_stash{stash_order[2]}_vault"
    return hashlib.sha1(role_str.encode("utf-8")).hexdigest()

def main():
    s = requests.Session()
    data = s.post(f"{BASE_URL}/session", json={}).json()
    session_id, token, stash_order = data["session_id"], data["token"], data["stash_order"]

    checkpoints = ["heat5", f"stash{stash_order[0]}", f"stash{stash_order[1]}", f"stash{stash_order[2]}", "vault"]
    for step in checkpoints:
        time.sleep(6.5) # Bypass 6.0s anti-cheat threshold
        sig = sign(f"{session_id}|{step}|{token}")
        cp_data = s.post(f"{BASE_URL}/checkpoint", json={"session_id": session_id, "step": step, "token": token, "sig": sig}).json()
        token = cp_data["token"]

    staff_role = derive_staff_role(stash_order)
    time.sleep(6.5)
    claim_sig = sign(f"{session_id}|claim|{token}")
    resp = s.post(f"{BASE_URL}/claim", json={"session_id": session_id, "role": staff_role, "token": token, "sig": claim_sig})
    print(resp.text)

if __name__ == "__main__":
    main()
```

Executing `script.py` successfully returns the staff flag upon completion.

---

## 🛡️ Remediation
1. **Server-Authoritative Cryptography:** Never embed private cryptographic signing keys in client-side binaries or assemblies.
2. **Complete Signature Coverage:** Include all transaction parameters (such as `role`) inside the HMAC signed data payload to prevent parameter tampering.
3. **Server-Side Session Validation:** Maintain and verify user role permissions exclusively within server-side session state rather than accepting client-supplied role values.
