# Encryption Tool - Quick Start Guide

## What This Tool Does
Encrypts and decrypts files using AES-256, the same encryption standard used by governments and banks.

## Quick Start

### Option 1: User-Friendly GUI (Recommended)

```bash
python main.py
```

Then:
1. Click **Browse** next to "Select File to Encrypt/Decrypt"
2. Pick any file you want to encrypt
3. Output filename auto-fills (add `.enc` if decrypting)
4. Enter a strong password
5. Confirm the password (must match)
6. Click **Encrypt File** or **Decrypt File**
7. Check the status box for results

### Option 2: Command Line

**Encrypt:**
```bash
python cli.py encrypt -i myfile.txt -o myfile.txt.enc -p "MyPassword123"
```

**Decrypt:**
```bash
python cli.py decrypt -i myfile.txt.enc -o myfile.txt -p "MyPassword123"
```

## How It Works

### Encryption Process
1. Takes your password and creates a secure key
2. Generates a random initialization vector (IV)
3. Encrypts your file using AES-256-CBC
4. Saves: salt + IV + encrypted data
5. **Result:** Unreadable file that only opens with correct password

### Decryption Process
1. Reads the stored salt and IV from encrypted file
2. Recreates the key using your password
3. Decrypts the data
4. **Result:** Original file is restored perfectly

## Key Features

| Feature | Benefit |
|---------|---------|
| AES-256 Encryption | Military-grade security |
| Password-based | No key files to lose |
| Works on any file | Documents, images, archives, etc. |
| Large file support | Handles multi-GB files |
| Cross-platform | Windows, Mac, Linux |
| Simple GUI | No technical knowledge needed |
| CLI available | Perfect for automation |

## Security Tips

✓ Use **12+ character** passwords  
✓ Mix uppercase, lowercase, numbers, symbols  
✓ Don't share passwords via email  
✓ Use different passwords for different files  
✓ Delete original files after encryption (optional)  
✓ Keep encrypted files as backups  

### Bad Passwords ❌
- password
- 123456
- qwerty
- Your birthday

### Good Passwords ✓
- MyDog#Loves$Coffee2024
- SecureFile!Pass@2024
- P@ssw0rd$UltraSecure!
- Coffee#2024$Money!Bank

## Troubleshooting

### "Incorrect password" when decrypting
→ Check if you're using the right password (case-sensitive)

### File won't open after decryption
→ Make sure you're using the exact same password

### GUI doesn't start
→ Run: `pip install cryptography`

### Large file taking long time
→ Normal! Check the progress bar, files are being processed

## Examples

### Protect a Word Document
```bash
python cli.py encrypt -i report.docx -o report.docx.enc -p "MyCompanySecret123!"
```

### Backup Sensitive Data
```bash
python cli.py encrypt -i mydata.zip -o mydata.zip.enc -p "BackupKey2024!"
```

### Decrypt for Use
```bash
python cli.py decrypt -i mydata.zip.enc -o mydata.zip -p "BackupKey2024!"
```

## Files in This Package

| File | Purpose |
|------|---------|
| `main.py` | Launches the GUI |
| `gui.py` | The user interface |
| `encryption_engine.py` | Core encryption logic |
| `cli.py` | Command-line tool |
| `requirements.txt` | Dependencies |
| `README.md` | Full documentation |

## Technical Details (Optional)

- **Algorithm:** AES-256-CBC
- **Key Derivation:** PBKDF2-HMAC-SHA256 (100,000 iterations)
- **Padding:** PKCS7
- **IV:** 16 random bytes per file

## Getting Help

1. Check the log box in the GUI for error messages
2. CLI shows detailed error messages
3. Verify file paths and passwords
4. Ensure file isn't already encrypted/decrypted

---

**Version:** 1.0  
**Status:** Production Ready ✓
