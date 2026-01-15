# Advanced Encryption Tool - AES-256

**Company Name:** CODTECH IT SOLUTIONS PRIVATE LIMITED

**Intern Name:** SARVEPALLI AUDI SIVA BHANUVARDHAN

**Intern ID:** CTIS2221

**Domain:** CYBERSECURITY & ETHICAL HACKING

**Batch Duration:** 4 WEEKS

**Mentor Name:** NEELA SANTHOSH KUMAR

## Project Overview

A robust file encryption and decryption application using AES-256-CBC algorithm with both GUI and CLI interfaces.

## Features

✓ **AES-256-CBC Encryption** - Military-grade encryption algorithm

✓ **Password-Based Key Derivation** - PBKDF2 with 100,000 iterations

✓ **User-Friendly GUI** - Simple tkinter interface

✓ **Command-Line Interface** - For batch operations

✓ **Large File Support** - Handles files of any size with streaming

✓ **Secure Random IV** - New IV for each encryption

✓ **Password Confirmation** - Prevents accidental password errors

✓ **Error Handling** - Comprehensive error messages

✓ **Progress Feedback** - Status updates during operations

## Installation

### Requirements
- Python 3.7+
- cryptography library

### Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### GUI Mode (Recommended)

```bash
python main.py
```

Or simply:

```bash
python gui.py
```

**Steps:**
1. Click "Browse" to select the file to encrypt/decrypt
2. Click "Browse" for output file (or auto-generated)
3. Enter encryption password
4. Confirm password
5. Click "Encrypt File" or "Decrypt File"
6. View status in the log area

### Command-Line Mode

**Encrypt a file:**
```bash
python cli.py encrypt -i document.pdf -o document.pdf.enc -p "mypassword"
```

**Decrypt a file:**
```bash
python cli.py decrypt -i document.pdf.enc -o document.pdf -p "mypassword"
```

## Security Details

### Encryption Specification
- **Algorithm**: AES-256-CBC
- **Key Size**: 256 bits (32 bytes)
- **Block Size**: 128 bits (16 bytes)
- **Padding**: PKCS7
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **IV**: 16 bytes of random data per file

### File Format
```
[Salt: 16 bytes] [IV: 16 bytes] [Encrypted Data: variable]
```

The salt and IV are stored unencrypted with the ciphertext, which is standard practice and necessary for decryption.

## Security Recommendations

1. **Use Strong Passwords**: Minimum 12 characters with mixed case, numbers, and symbols
2. **Unique Passwords**: Use different passwords for different files
3. **Backup Keys**: Consider keeping a secure backup of important passwords
4. **Secure Deletion**: Use secure file deletion for original files after encryption
5. **Transport**: Encrypt files before sending over untrusted networks

## File Size Handling

- Supports files of any size
- Uses 1MB streaming buffer for memory efficiency
- No size limitations

## Testing

### Example: Create and Encrypt a Test File

```bash
# Create a test file
echo "This is a secret message" > secret.txt

# Encrypt it
python cli.py encrypt -i secret.txt -o secret.txt.enc -p "MySecure123!"

# Verify encryption (file should be unreadable)
type secret.txt.enc

# Decrypt it
python cli.py decrypt -i secret.txt.enc -o secret_restored.txt -p "MySecure123!"

# Verify decryption
type secret_restored.txt
```

## Troubleshooting

### "Incorrect password" Error
- Ensure you're using the same password that was used for encryption
- Check for extra spaces or caps lock
- Passwords are case-sensitive

### "Invalid encrypted file format" Error
- The file may be corrupted
- The file may not have been encrypted with this tool
- Try using the original encrypted file

### GUI won't start
- Ensure tkinter is installed: `pip install tk`
- On Linux: `sudo apt-get install python3-tk`

## Architecture

```
main.py          -> Entry point
├── gui.py       -> User interface (tkinter)
└── encryption_engine.py -> Core encryption logic
cli.py           -> Command-line interface
```

## Performance

- **Small files** (< 10MB): < 1 second
- **Large files** (1GB+): Progressive encryption with no memory issues
- **Bottleneck**: Disk I/O and PBKDF2 key derivation

## out put
<img width="757" height="659" alt="Image" src="https://github.com/user-attachments/assets/dfc7607c-9ec9-4425-ab3c-ad1335b0a50e" />

<img width="1187" height="803" alt="Image" src="https://github.com/user-attachments/assets/f6637b44-90db-47ed-bb99-ecd52f1432b9" />

<img width="1156" height="758" alt="Image" src="https://github.com/user-attachments/assets/b64160af-4641-4abc-8737-79b9f9780a11" />

## License

Open source - Use freely for personal and commercial projects.

## Support

For issues or questions, refer to the logging output for detailed error messages.
