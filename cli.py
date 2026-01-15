"""
Command-line interface for encryption/decryption
Alternative to GUI for batch operations
"""

import argparse
import sys
from encryption_engine import EncryptionEngine


def main():
    parser = argparse.ArgumentParser(
        description="AES-256 File Encryption Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Encrypt a file:
    python cli.py encrypt -i secret.txt -o secret.txt.enc -p mypassword
  
  Decrypt a file:
    python cli.py decrypt -i secret.txt.enc -o secret.txt -p mypassword
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('-i', '--input', required=True, help='Input file path')
    encrypt_parser.add_argument('-o', '--output', required=True, help='Output file path')
    encrypt_parser.add_argument('-p', '--password', required=True, help='Encryption password')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('-i', '--input', required=True, help='Input file path')
    decrypt_parser.add_argument('-o', '--output', required=True, help='Output file path')
    decrypt_parser.add_argument('-p', '--password', required=True, help='Decryption password')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'encrypt':
        print(f"Encrypting {args.input}...")
        result = EncryptionEngine.encrypt_file(args.input, args.output, args.password)
        print(f"Status: {result['status'].upper()}")
        print(f"Message: {result['message']}")
        if result['status'] == 'success':
            print(f"Original size: {result['input_size']:,} bytes")
            print(f"Encrypted size: {result['output_size']:,} bytes")
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.command == 'decrypt':
        print(f"Decrypting {args.input}...")
        result = EncryptionEngine.decrypt_file(args.input, args.output, args.password)
        print(f"Status: {result['status'].upper()}")
        print(f"Message: {result['message']}")
        if result['status'] == 'success':
            print(f"Decrypted size: {result['output_size']:,} bytes")
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
