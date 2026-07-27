import socket
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SERVER_IP = "10.49.170.119"
SERVER_PORT = 4000

def solve():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)

    try:
        # 1. Send 'hello'
        sock.sendto(b"hello", (SERVER_IP, SERVER_PORT))
        print(sock.recvfrom(4096)[0].decode())

        # 2. Send 'ready' to get instructions
        sock.sendto(b"ready", (SERVER_IP, SERVER_PORT))
        instructions = sock.recvfrom(4096)[0]
        print(f"[+] Instructions: {instructions}")

        key = b"thisisaverysecretkeyl337"
        nonce = b"secureivl337"
        
    
        checksum_target_bytes = instructions.split(b"checksum of ")[1].split(b" send final")[0]
        checksum_hex = checksum_target_bytes.hex()

        aesgcm = AESGCM(key)

        print("[*] Brute-forcing/fetching flags until checksum matches...")
        while True:
            sock.sendto(b"final", (SERVER_IP, SERVER_PORT))
            ciphertext = sock.recvfrom(4096)[0]

            sock.sendto(b"final", (SERVER_IP, SERVER_PORT))
            tag = sock.recvfrom(4096)[0]

            try:
                plaintext = aesgcm.decrypt(nonce, ciphertext + tag, None)
                
                # Verify SHA256 checksum
                if hashlib.sha256(plaintext).hexdigest() == checksum_hex:
                    print(f"\n[+] SUCCESS! Found the flag: {plaintext.decode()}")
                    break
            except Exception:
                # Ignore decryption/tag verification failures on decoy flags
                continue

    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    solve()