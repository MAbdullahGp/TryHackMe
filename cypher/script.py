# Read the encrypted message from message.txt
with open("message.txt", "r") as f:
    ciphertext = f.read()

def dec(ciphertext):
    return "".join(
        chr((ord(c) - (base := ord('A' ) if c.isupper() else ord('a')) - i) % 26 + base)
        if c.isalpha() else c
        for i, c in enumerate(ciphertext)
    )

flag = dec(ciphertext)
print(f"Decoded Flag: {flag}")
