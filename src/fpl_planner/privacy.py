"""Authenticated personal-report encryption; raw inputs never enter git."""
import base64
import hashlib
import hmac
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b'FPL1'


def key_bytes(key):
    try:
        raw = base64.b64decode(key, altchars=b'-_', validate=True)
        if len(raw) != 32:
            raise ValueError()
        return raw
    except (ValueError, TypeError):
        raise ValueError('Invalid report encryption key') from None


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def fingerprint(value, key):
    return hmac.new(key_bytes(key), canonical(value), hashlib.sha256).hexdigest()


def seal(report, key):
    nonce = os.urandom(12)
    return MAGIC + nonce + AESGCM(key_bytes(key)).encrypt(nonce, canonical(report), MAGIC)


def unseal(data, key):
    if not data.startswith(MAGIC) or len(data) < 32:
        raise ValueError('Invalid encrypted report')
    return json.loads(AESGCM(key_bytes(key)).decrypt(data[4:16], data[16:], MAGIC))
