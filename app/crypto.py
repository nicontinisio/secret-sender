import os, base64, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from fastapi import HTTPException
from .config import settings


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def encrypt(data: bytes, password: str = None) -> dict:
    if password:
        salt = os.urandom(16)
        key = _derive_key(password, salt)
        sk = base64.b64encode(salt).decode()
        enc_pw = True
    else:
        key = os.urandom(32)
        sk = base64.b64encode(key).decode()
        enc_pw = False
    iv = os.urandom(12)
    aes = AESGCM(key)
    ct = aes.encrypt(iv, data, None)
    return {"iv": base64.b64encode(iv).decode(),
            "ct": base64.b64encode(ct).decode(),
            "sk": sk,
            "enc_pw": enc_pw}


def decrypt(blob: dict, password: str = None) -> bytes:
    iv = base64.b64decode(blob['iv'])
    ct = base64.b64decode(blob['ct'])
    if blob['enc_pw']:
        if not password:
            raise HTTPException(401, "Password richiesta")
        salt = base64.b64decode(blob['sk'])
        key = _derive_key(password, salt)
    else:
        key = base64.b64decode(blob['sk'])
    aes = AESGCM(key)
    try:
        return aes.decrypt(iv, ct, None)
    except Exception:
        raise HTTPException(403, "Password non valida o dati corrotti")