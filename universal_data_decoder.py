import sys
import base64
import binascii
import zlib
import gzip
import json
import urllib.parse
import re

def analyze_and_decode(data_input):
    print("=" * 80)
    print("🔍 UNIVERSAL DATA & CIPHERTEXT DETECTIVE REPORT")
    print("=" * 80)
    
    if isinstance(data_input, str):
        text = data_input.strip()
        raw_bytes = text.encode('utf-8', errors='ignore')
    else:
        raw_bytes = data_input
        text = raw_bytes.decode('utf-8', errors='ignore')

    print(f"• Input Length: {len(text)} characters ({len(raw_bytes)} bytes)")
    print(f"• Sample Preview: {text[:80]}...\n")
    
    findings = []

    # 1. Check if URL Encoded
    if '%' in text and re.search(r'%[0-9a-fA-F]{2}', text):
        try:
            unquoted = urllib.parse.unquote(text)
            if unquoted != text:
                findings.append(("URL / Percent Encoding", unquoted))
        except Exception:
            pass

    # 2. Check if JSON Web Token (JWT)
    jwt_match = re.match(r'^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$', text)
    if jwt_match:
        parts = text.split('.')
        try:
            # Decode Header and Payload
            def b64_decode(p):
                rem = len(p) % 4
                if rem:
                    p += '=' * (4 - rem)
                return json.loads(base64.urlsafe_b64decode(p).decode('utf-8'))
            header = b64_decode(parts[0])
            payload = b64_decode(parts[1])
            findings.append(("JSON Web Token (JWT)", f"Header: {json.dumps(header, indent=2)}\nPayload: {json.dumps(payload, indent=2)}"))
        except Exception:
            pass

    # 3. Check if Hexadecimal
    clean_hex = text.replace(" ", "").replace("0x", "").replace(":", "")
    if re.fullmatch(r'[0-9a-fA-F]+', clean_hex) and len(clean_hex) % 2 == 0:
        try:
            hex_bytes = binascii.unhexlify(clean_hex)
            ascii_text = hex_bytes.decode('utf-8', errors='ignore')
            findings.append((f"Hexadecimal (Raw {len(hex_bytes)} bytes)", f"Hex Decoded ASCII: {ascii_text[:200]}"))
            
            # Check if hex bytes are zlib compressed (PDF FlateDecode: 78 9c or 78 01)
            if hex_bytes.startswith(b'\x78\x9c') or hex_bytes.startswith(b'\x78\x01') or hex_bytes.startswith(b'\x78\xda'):
                try:
                    decompressed = zlib.decompress(hex_bytes).decode('utf-8', errors='ignore')
                    findings.append(("Zlib / PDF FlateDecode Stream (from Hex)", decompressed[:400]))
                except Exception:
                    pass
        except Exception:
            pass

    # 4. Check if Base64
    clean_b64 = text.replace("\n", "").replace("\r", "").strip()
    if re.match(r'^[A-Za-z0-9+/=_-]+$', clean_b64) and len(clean_b64) >= 4:
        try:
            rem = len(clean_b64) % 4
            if rem:
                clean_b64 += '=' * (4 - rem)
            b64_bytes = base64.b64decode(clean_b64)
            
            # Try plain text
            b64_text = b64_bytes.decode('utf-8', errors='ignore')
            if any(c.isprintable() for c in b64_text):
                findings.append(("Base64 Encoded Text", b64_text[:300]))

            # Check if Base64 contains GZIP (Magic bytes 1F 8B)
            if b64_bytes.startswith(b'\x1f\x8b'):
                try:
                    decompressed = gzip.decompress(b64_bytes).decode('utf-8', errors='ignore')
                    findings.append(("GZIP Compressed inside Base64", decompressed[:400]))
                except Exception:
                    pass

            # Check if Base64 contains Zlib / PDF Flate stream (78 9C)
            if b64_bytes.startswith(b'\x78\x9c') or b64_bytes.startswith(b'\x78\x01') or b64_bytes.startswith(b'\x78\xda'):
                try:
                    decompressed = zlib.decompress(b64_bytes).decode('utf-8', errors='ignore')
                    findings.append(("Zlib / PDF FlateStream inside Base64", decompressed[:400]))
                except Exception:
                    pass
        except Exception:
            pass

    # 5. Check if Base85 / ASCII85 (Standard in PDF objects)
    try:
        b85_bytes = base64.a85decode(text.encode('ascii'))
        findings.append(("ASCII85 (PDF Stream Encoding)", b85_bytes.decode('utf-8', errors='ignore')[:300]))
    except Exception:
        pass

    # 6. Check if One-Way Cryptographic Hash
    if len(text) == 32 and re.fullmatch(r'[0-9a-fA-F]{32}', text):
        findings.append(("MD5 Hash (One-Way)", "This is a 128-bit MD5 hash. Hashes cannot be mathematically decrypted (must use lookup/rainbow tables)."))
    elif len(text) == 40 and re.fullmatch(r'[0-9a-fA-F]{40}', text):
        findings.append(("SHA-1 Hash (One-Way)", "This is a 160-bit SHA-1 hash (one-way)."))
    elif len(text) == 64 and re.fullmatch(r'[0-9a-fA-F]{64}', text):
        findings.append(("SHA-256 Hash (One-Way)", "This is a 256-bit SHA-256 hash (one-way)."))
    elif text.startswith('$2a$') or text.startswith('$2b$') or text.startswith('$2y$'):
        findings.append(("Bcrypt Password Hash", "This is a salted Bcrypt password hash. Irreversible by design."))

    # Output Findings
    if findings:
        print(f"✅ IDENTIFIED {len(findings)} POSSIBLE DECODING FORMAT(S):\n")
        for idx, (fmt, result) in enumerate(findings, 1):
            print(f"--- [FORMAT {idx}: {fmt}] ---")
            print(result)
            print()
    else:
        print("🔒 RESULT: HIGH-ENTROPY RAW CIPHERTEXT (AES / RSA / CHACHA20)")
        print("The data appears to be true cryptographic ciphertext (not simple Base64/Hex/Gzip).")
        print("To decrypt real ciphertext, you need:")
        print("  1. The Algorithm (e.g., AES-256-CBC, AES-GCM, RSA)")
        print("  2. The Secret Key (e.g., 256-bit AES key, or RSA Private Key)")
        print("  3. The Initialization Vector (IV / Nonce) if using symmetric cipher.")

    print("=" * 80)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_input = " ".join(sys.argv[1:])
        analyze_and_decode(test_input)
    else:
        print("Usage: python universal_data_decoder.py \"<paste_your_encrypted_or_encoded_string>\"")
        print("\nEntering interactive mode. Paste your string below and press Enter:\n")
        try:
            user_str = input("Paste data: ")
            if user_str.strip():
                analyze_and_decode(user_str)
        except KeyboardInterrupt:
            pass
