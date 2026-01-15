"""
AES-256 Encryption Engine
Handles encryption and decryption of files using AES-256-CBC
"""

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding


class EncryptionEngine:
    """AES-256 encryption/decryption engine"""
    
    BLOCK_SIZE = 128
    KEY_SIZE = 32  # 256 bits for AES-256
    BUFFER_SIZE = 1024 * 1024  # 1MB buffer for large files
    
    @staticmethod
    def derive_key_from_password(password: str, salt: bytes = None) -> tuple:
        """
        Derive a 256-bit key from a password using PBKDF2-like approach
        Returns: (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        # Use PBKDF2 with SHA-256
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return key[:EncryptionEngine.KEY_SIZE], salt
    
    @staticmethod
    def encrypt_file(input_file: str, output_file: str, password: str) -> dict:
        """
        Encrypt a file using AES-256-CBC
        
        Args:
            input_file: Path to file to encrypt
            output_file: Path to save encrypted file
            password: Password for encryption
            
        Returns:
            dict with status, message, and metadata
        """
        try:
            if not os.path.exists(input_file):
                return {"status": "error", "message": "Input file not found"}
            
            # Generate key and IV
            key, salt = EncryptionEngine.derive_key_from_password(password)
            iv = os.urandom(16)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            padder = sym_padding.PKCS7(EncryptionEngine.BLOCK_SIZE).padder()
            
            # Write salt and IV to output file (unencrypted, needed for decryption)
            with open(output_file, 'wb') as out_f:
                out_f.write(salt)
                out_f.write(iv)
                
                # Encrypt file in chunks
                with open(input_file, 'rb') as in_f:
                    while True:
                        chunk = in_f.read(EncryptionEngine.BUFFER_SIZE)
                        if not chunk:
                            break
                        
                        padded_chunk = padder.update(chunk)
                        encrypted_chunk = encryptor.update(padded_chunk)
                        out_f.write(encrypted_chunk)
                    
                    # Finalize padding
                    padded_final = padder.finalize()
                    encrypted_final = encryptor.update(padded_final)
                    encrypted_final += encryptor.finalize()
                    out_f.write(encrypted_final)
            
            file_size = os.path.getsize(input_file)
            return {
                "status": "success",
                "message": f"File encrypted successfully",
                "input_size": file_size,
                "output_size": os.path.getsize(output_file)
            }
        
        except Exception as e:
            return {"status": "error", "message": f"Encryption failed: {str(e)}"}
    
    @staticmethod
    def decrypt_file(input_file: str, output_file: str, password: str) -> dict:
        """
        Decrypt a file encrypted with AES-256-CBC
        
        Args:
            input_file: Path to encrypted file
            output_file: Path to save decrypted file
            password: Password for decryption
            
        Returns:
            dict with status and message
        """
        try:
            if not os.path.exists(input_file):
                return {"status": "error", "message": "Input file not found"}
            
            with open(input_file, 'rb') as in_f:
                # Read salt and IV
                salt = in_f.read(16)
                iv = in_f.read(16)
                
                if len(salt) != 16 or len(iv) != 16:
                    return {"status": "error", "message": "Invalid encrypted file format"}
                
                # Derive key using same salt
                key, _ = EncryptionEngine.derive_key_from_password(password, salt)
                
                # Create cipher
                cipher = Cipher(
                    algorithms.AES(key),
                    modes.CBC(iv),
                    backend=default_backend()
                )
                decryptor = cipher.decryptor()
                unpadder = sym_padding.PKCS7(EncryptionEngine.BLOCK_SIZE).unpadder()
                
                # Decrypt file in chunks
                with open(output_file, 'wb') as out_f:
                    while True:
                        chunk = in_f.read(EncryptionEngine.BUFFER_SIZE)
                        if not chunk:
                            break
                        
                        decrypted_chunk = decryptor.update(chunk)
                        unpadded_chunk = unpadder.update(decrypted_chunk)
                        out_f.write(unpadded_chunk)
                    
                    # Finalize decryption
                    decrypted_final = decryptor.finalize()
                    unpadded_final = unpadder.update(decrypted_final)
                    unpadded_final += unpadder.finalize()
                    out_f.write(unpadded_final)
            
            return {
                "status": "success",
                "message": "File decrypted successfully",
                "output_size": os.path.getsize(output_file)
            }
        
        except ValueError as e:
            if "bad decrypt" in str(e).lower():
                return {"status": "error", "message": "Decryption failed: Incorrect password"}
            return {"status": "error", "message": f"Decryption failed: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Decryption failed: {str(e)}"}
