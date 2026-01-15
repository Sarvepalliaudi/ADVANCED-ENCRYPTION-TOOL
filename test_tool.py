"""
Test suite for the encryption tool
Demonstrates all features and verifies they work correctly
"""

import os
import sys
from encryption_engine import EncryptionEngine
import hashlib


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test(test_name, passed, message=""):
    """Print test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if message:
        print(f"       {message}")


def test_small_file():
    """Test encrypting a small text file"""
    print_header("Test 1: Small Text File Encryption")
    
    # Create test file
    test_content = "Hello, this is a small test file for encryption!"
    test_file = "test_small.txt"
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    enc_file = "test_small.txt.enc"
    dec_file = "test_small_restored.txt"
    password = "TestPassword123!"
    
    # Encrypt
    result = EncryptionEngine.encrypt_file(test_file, enc_file, password)
    passed = result["status"] == "success"
    print_test("File encryption", passed, result["message"])
    
    # Decrypt
    result = EncryptionEngine.decrypt_file(enc_file, dec_file, password)
    passed = result["status"] == "success"
    print_test("File decryption", passed, result["message"])
    
    # Verify content
    with open(dec_file, 'r') as f:
        restored_content = f.read()
    
    content_matches = restored_content == test_content
    print_test("Content verification", content_matches, 
              f"Original: {test_content[:30]}... Restored: {restored_content[:30]}...")
    
    # Cleanup
    os.remove(test_file)
    os.remove(enc_file)
    os.remove(dec_file)
    
    return content_matches


def test_binary_file():
    """Test encrypting a binary file"""
    print_header("Test 2: Binary File Encryption")
    
    # Create binary test file
    test_file = "test_binary.bin"
    binary_data = bytes(range(256))  # 256 bytes of data
    with open(test_file, 'wb') as f:
        f.write(binary_data)
    
    enc_file = "test_binary.bin.enc"
    dec_file = "test_binary_restored.bin"
    password = "BinarySecret456!"
    
    # Encrypt
    result = EncryptionEngine.encrypt_file(test_file, enc_file, password)
    passed = result["status"] == "success"
    print_test("Binary file encryption", passed, result["message"])
    
    # Decrypt
    result = EncryptionEngine.decrypt_file(enc_file, dec_file, password)
    passed = result["status"] == "success"
    print_test("Binary file decryption", passed, result["message"])
    
    # Verify content
    with open(dec_file, 'rb') as f:
        restored_data = f.read()
    
    data_matches = restored_data == binary_data
    print_test("Binary content verification", data_matches,
              f"Size: {len(binary_data)} bytes → {len(restored_data)} bytes")
    
    # Cleanup
    os.remove(test_file)
    os.remove(enc_file)
    os.remove(dec_file)
    
    return data_matches


def test_large_file():
    """Test encrypting a larger file"""
    print_header("Test 3: Large File Encryption (10MB)")
    
    # Create large test file
    test_file = "test_large.bin"
    large_size = 10 * 1024 * 1024  # 10MB
    with open(test_file, 'wb') as f:
        # Write in chunks
        chunk = b"0" * (1024 * 1024)
        for i in range(10):
            f.write(chunk)
    
    enc_file = "test_large.bin.enc"
    dec_file = "test_large_restored.bin"
    password = "LargeFilePassword789!"
    
    # Encrypt
    result = EncryptionEngine.encrypt_file(test_file, enc_file, password)
    passed = result["status"] == "success"
    print_test("Large file encryption", passed, 
              f"Size: {result['input_size']:,} → {result['output_size']:,} bytes")
    
    # Decrypt
    result = EncryptionEngine.decrypt_file(enc_file, dec_file, password)
    passed = result["status"] == "success"
    print_test("Large file decryption", passed, result["message"])
    
    # Verify checksums instead of content
    with open(test_file, 'rb') as f:
        original_hash = hashlib.sha256(f.read()).hexdigest()
    
    with open(dec_file, 'rb') as f:
        restored_hash = hashlib.sha256(f.read()).hexdigest()
    
    hash_matches = original_hash == restored_hash
    print_test("Large file integrity", hash_matches,
              f"SHA256 checksum matches")
    
    # Cleanup
    os.remove(test_file)
    os.remove(enc_file)
    os.remove(dec_file)
    
    return hash_matches


def test_wrong_password():
    """Test that wrong password fails"""
    print_header("Test 4: Wrong Password Detection")
    
    # Create test file
    test_file = "test_wrongpass.txt"
    with open(test_file, 'w') as f:
        f.write("Secret data that should not be readable with wrong password")
    
    enc_file = "test_wrongpass.txt.enc"
    dec_file = "test_wrongpass_restored.txt"
    password = "CorrectPassword123!"
    wrong_password = "WrongPassword456!"
    
    # Encrypt with correct password
    EncryptionEngine.encrypt_file(test_file, enc_file, password)
    
    # Try to decrypt with wrong password
    result = EncryptionEngine.decrypt_file(enc_file, dec_file, wrong_password)
    wrong_pass_failed = result["status"] == "error"
    print_test("Wrong password rejection", wrong_pass_failed,
              f"Error: {result['message']}")
    
    # Cleanup
    os.remove(test_file)
    os.remove(enc_file)
    
    return wrong_pass_failed


def test_multiple_encryptions():
    """Test that same file encrypted twice produces different results"""
    print_header("Test 5: Random IV Verification")
    
    # Create test file
    test_file = "test_random.txt"
    with open(test_file, 'w') as f:
        f.write("Same content, different encryptions")
    
    enc_file1 = "test_random_1.enc"
    enc_file2 = "test_random_2.enc"
    password = "SamePassword123!"
    
    # Encrypt same file twice
    EncryptionEngine.encrypt_file(test_file, enc_file1, password)
    EncryptionEngine.encrypt_file(test_file, enc_file2, password)
    
    # Read encrypted files
    with open(enc_file1, 'rb') as f:
        enc_content1 = f.read()
    
    with open(enc_file2, 'rb') as f:
        enc_content2 = f.read()
    
    # Should be different due to random IV
    different = enc_content1 != enc_content2
    print_test("Different IV per encryption", different,
              "Two encryptions of same file produce different ciphertext")
    
    # Cleanup
    os.remove(test_file)
    os.remove(enc_file1)
    os.remove(enc_file2)
    
    return different


def test_corrupted_file():
    """Test that corrupted encrypted file is detected"""
    print_header("Test 6: Corrupted File Detection")
    
    # Create and encrypt a file
    test_file = "test_corrupt.txt"
    with open(test_file, 'w') as f:
        f.write("Data to be encrypted")
    
    enc_file = "test_corrupt.enc"
    password = "Password123!"
    
    EncryptionEngine.encrypt_file(test_file, enc_file, password)
    
    # Corrupt the file by modifying bytes
    with open(enc_file, 'r+b') as f:
        f.seek(50)
        f.write(b"CORRUPTED")
    
    # Try to decrypt corrupted file
    dec_file = "test_corrupt_restored.txt"
    result = EncryptionEngine.decrypt_file(enc_file, dec_file, password)
    corruption_detected = result["status"] == "error"
    print_test("Corrupted file detection", corruption_detected,
              "Decryption fails on corrupted data")
    
    # Cleanup
    os.remove(test_file)
    os.remove(enc_file)
    
    return corruption_detected


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  ENCRYPTION TOOL - TEST SUITE".center(68) + "║")
    print("║" + "  Testing AES-256 Encryption/Decryption".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = []
    
    try:
        results.append(("Small File", test_small_file()))
        results.append(("Binary File", test_binary_file()))
        results.append(("Large File", test_large_file()))
        results.append(("Wrong Password", test_wrong_password()))
        results.append(("Random IV", test_multiple_encryptions()))
        results.append(("Corrupted File", test_corrupted_file()))
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        return False
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Tool is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
