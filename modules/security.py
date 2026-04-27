# =============================================================================
# security.py
# -----------------------------------------------------------------------------
# Indeholder 3 AES krypteringsmetoder.
# Vi vælger én til vores pipeline — se begrundelse nederst.
# =============================================================================

import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.fernet import Fernet

# 32 bytes = AES-256 nøgle (hardcodet til simpelhed — aldrig i produktion!)
AES_KEY = b'12345678901234567890123456789012'
FERNET_KEY = base64.urlsafe_b64encode(AES_KEY)


# AES-GCM
def encrypt_gcm(plaintext: str) -> str:
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(12)  # Unik nonce for hver kryptering
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return base64.urlsafe_b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_gcm(token: str) -> str:
    raw = base64.urlsafe_b64decode(token.encode('utf-8'))
    nonce, ciphertext = raw[:12], raw[12:]
    return AESGCM(AES_KEY).decrypt(nonce, ciphertext, None).decode('utf-8')

# AES-CBC
def encrypt_cbc(plaintext: str) -> str:
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv))
    ciphertext = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
    return base64.urlsafe_b64encode(iv + ciphertext).decode('utf-8')

def decrypt_cbc(token: str) -> str:
    raw = base64.urlsafe_b64decode(token.encode('utf-8'))
    iv, ciphertext = raw[:16], raw[16:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv))
    padded = cipher.decryptor().update(ciphertext) + cipher.decryptor().finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(padded) + unpadder.finalize()).decode('utf-8')


# AES-CBC med Fernet
def encrypt_fernet(plaintext: str) -> str:
    return Fernet(FERNET_KEY).encrypt(plaintext.encode('utf-8')).decode('utf-8')

def decrypt_fernet(token: str) -> str:
    return Fernet(FERNET_KEY).decrypt(token.encode('utf-8')).decode('utf-8')


def encrypt(plaintext: str) -> str:
    return encrypt_gcm(plaintext)

def decrypt(ciphertext: str) -> str:
    return decrypt_gcm(ciphertext)