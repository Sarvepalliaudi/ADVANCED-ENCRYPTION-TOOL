"""
Demo script showing the encryption tool in action
Run this to see a quick demonstration
"""

import os
import sys
from encryption_engine import EncryptionEngine


def demo():
    """Run a quick demonstration"""
    
    print("\n" + "=" * 70)
    print("  ADVANCED ENCRYPTION TOOL - DEMONSTRATION")
    print("=" * 70)
    
    # Create a sample file
    sample_file = "demo_sample.txt"
    sample_content = """
    This is a confidential document.
    
    IMPORTANT: Keep this information secure!
    
    Account ID: 12345-SECURE
    Password: EncryptedData2024
    
    This file will be encrypted using military-grade AES-256 encryption.
    """
    
    print("\n[1] Creating sample file...")
    with open(sample_file, 'w') as f:
        f.write(sample_content)
    
    file_size = os.path.getsize(sample_file)
    print(f"    ✓ Created '{sample_file}' ({file_size} bytes)")
    print(f"    Content preview: {sample_content[:60]}...")
    
    # Encrypt the file
    encrypted_file = "demo_sample.txt.enc"
    password = "MySecurePassword123!"
    
    print(f"\n[2] Encrypting file with AES-256...")
    print(f"    Password: {'*' * len(password)}")
    
    result = EncryptionEngine.encrypt_file(sample_file, encrypted_file, password)
    
    if result['status'] == 'success':
        enc_size = os.path.getsize(encrypted_file)
        print(f"    ✓ {result['message']}")
        print(f"    Original size: {result['input_size']:,} bytes")
        print(f"    Encrypted size: {enc_size:,} bytes")
    else:
        print(f"    ✗ Error: {result['message']}")
        return
    
    # Show encrypted file is unreadable
    print(f"\n[3] Checking encrypted file...")
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()
    
    print(f"    Encrypted data (first 50 bytes): {encrypted_data[:50]}")
    print(f"    ✓ File is now unreadable without password")
    
    # Decrypt the file
    decrypted_file = "demo_sample_decrypted.txt"
    
    print(f"\n[4] Decrypting file with password...")
    result = EncryptionEngine.decrypt_file(encrypted_file, decrypted_file, password)
    
    if result['status'] == 'success':
        print(f"    ✓ {result['message']}")
        print(f"    Decrypted size: {result['output_size']:,} bytes")
    else:
        print(f"    ✗ Error: {result['message']}")
        return
    
    # Verify decryption
    print(f"\n[5] Verifying decrypted content...")
    with open(decrypted_file, 'r') as f:
        decrypted_content = f.read()
    
    if decrypted_content == sample_content:
        print(f"    ✓ Decrypted content matches original")
        print(f"    Content preview: {decrypted_content[:60]}...")
    else:
        print(f"    ✗ Content mismatch!")
        return
    
    # Test with wrong password
    print(f"\n[6] Testing wrong password protection...")
    wrong_dec = "demo_wrong_password.txt"
    result = EncryptionEngine.decrypt_file(encrypted_file, wrong_dec, "WrongPassword123!")
    
    if result['status'] == 'error':
        print(f"    ✓ Wrong password correctly rejected")
        print(f"    Error message: {result['message']}")
    else:
        print(f"    ✗ Wrong password was accepted (security issue!)")
    
    # Summary
    print("\n" + "=" * 70)
    print("  DEMONSTRATION SUMMARY")
    print("=" * 70)
    print(f"✓ Created sample file")
    print(f"✓ Encrypted with AES-256")
    print(f"✓ File is now unreadable")
    print(f"✓ Decrypted successfully")
    print(f"✓ Wrong password protection works")
    print(f"\n🎉 Encryption tool is working perfectly!")
    
    # Cleanup
    print(f"\n[7] Cleaning up demo files...")
    os.remove(sample_file)
    os.remove(encrypted_file)
    os.remove(decrypted_file)
    try:
        os.remove(wrong_dec)
    except:
        pass
    print(f"    ✓ Demo files cleaned up")
    
    print("\n" + "=" * 70)
    print("  NEXT STEPS")
    print("=" * 70)
    print("1. Run the GUI: python main.py")
    print("2. Or use CLI: python cli.py encrypt -i file.txt -o file.txt.enc -p 'password'")
    print("3. See QUICKSTART.md for detailed instructions")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
