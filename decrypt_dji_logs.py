#!/usr/bin/env python3
# Decryption script for the DJI-Android App Log-Folder (c) C.Peter 2026
# Licensed under GPLv3 License

import os
from base64 import b64decode
from Crypto.Cipher import AES
import string
import shutil
import unicodedata

# AES-Key and IV hardcoded according to the studies of: 
# https://www.synacktiv.com/publications/dji-android-go-4-application-security-analysis

key = bytes.fromhex("e9e856d55943731ac585dcda656f95c5")
iv  = bytes.fromhex("9d6c5cab5b0281255a222d1c861ddfdf")

# Check for Base64
def is_base64_line(line, threshold=0.9):
    line = line.strip().rstrip("=")
    if not line:
        return False
    base64_chars = set(string.ascii_letters + string.digits + "+/")
    valid = sum(1 for c in line if c in base64_chars)
    return (valid / len(line)) >= threshold

# Decrypt single file
def decrypt_file(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(input_path, "r") as f_in:
        lines = f_in.readlines()

    # Check encryption
    base64_lines = sum(is_base64_line(l) for l in lines)
    if base64_lines / max(1, len(lines)) < 0.5:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        shutil.copy2(input_path, output_path)
        print(f"Copied plaintext file: {input_path} -> {output_path}")
        return 

    with open(output_path, "w") as f_out:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            ct = b64decode(line)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = cipher.decrypt(ct)
            text = pt.decode(errors="replace").replace("\x00", "")
            text = sanitize_text(text)
            clean = "\n".join(l for l in text.splitlines() if l.strip())
            f_out.write(clean + "\n")

# Decrypt folder
def decrypt_folder(input_folder):
    parent_folder = os.path.abspath(input_folder)
    output_root = parent_folder + "_decrypted"

    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if not file.lower().endswith(".log"):
                continue  # nur Log-Dateien
            input_path = os.path.join(root, file)
            rel_path = os.path.relpath(input_path, parent_folder)
            output_path = os.path.join(output_root, rel_path)
            print(f"Processing {input_path} -> {output_path}")
            decrypt_file(input_path, output_path)

# Remove non printable symbols
def sanitize_text(text: str) -> str:
    return "".join(
        c for c in text
        if c == "\n" or c == "\t" or not unicodedata.category(c).startswith("C")
    )

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python decrypt_dji_logs.py <folder>")
        sys.exit(1)

    folder = sys.argv[1]
    decrypt_folder(folder)
