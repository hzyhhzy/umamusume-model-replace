from apsw import NotADBError
import io
from typing import BinaryIO

db_key_hex: str = "9C2BAB97BCF8C0C4F1A9EA7881A213F6C9EBF9D8D4C6A8E43CE5A259BDE7E9FD"
asset_key_bytes: bytes = bytes.fromhex("532B4631E4A7B9473E7CFB")

"""
Asset encryption
"""
def derive_pad(base_key: bytes, key_num: int) -> bytes:
    """
    shoutout to meeko, stole his pseudocode lol
    port of UmaJPManager.DerivePad:
      - key_num is treated as signed, 8-byte, little-endian
      - pad length = len(base_key) * 8
      - pad[i*8 + j] = base_key[i] ^ key_bytes[j]
    """
    if base_key is None or len(base_key) == 0:
        raise ValueError("base_key must be non-empty bytes")
    key_bytes = key_num.to_bytes(8, byteorder="little", signed=True)
    pad = bytearray(len(base_key) * 8)
    for i, kb in enumerate(base_key):
        for j in range(8):
            pad[i * 8 + j] = kb ^ key_bytes[j]
    return bytes(pad)

def xor_bytes_from_offset(buf: bytes, start_offset: int, pad: bytes) -> bytes:
    """
    returns XOR'ed bytes using input pad, starting from start_offset
    """
    if not buf or start_offset >= len(buf):
        return buf
    out = bytearray(buf)
    pad_len = len(pad)
    # absolute positions are the file positions (same as your reader)
    for abs_pos in range(start_offset, len(out)):
        out[abs_pos] ^= pad[abs_pos % pad_len]
    return bytes(out)

"""
DB encryption (based on APSW docs)
"""
def apply_db_encryption(db, **kwargs):
    """You must include an argument for keying, and optional cipher configurations"""

    if db.in_transaction:
        raise Exception("Won't update encryption while in a transaction")

    # the order of pragmas matters
    def pragma_order(item):
        # pragmas are case insensitive
        pragma = item[0].lower()
        # cipher must be first
        if pragma == "cipher":
            return 1
        # old default settings reset configuration next
        if pragma == "legacy":
            return 2
        # then anything with legacy in the name
        if "legacy" in pragma:
            return 3
        # all except keys
        if pragma not in {"key", "hexkey", "rekey", "hexrekey"}:
            return 3
        # keys are last
        return 100

    # check only ome key present
    if 1 != sum(1 if pragma_order(item) == 100 else 0 for item in kwargs.items()):
        raise ValueError("Exactly one key must be provided")

    for pragma, value in sorted(kwargs.items(), key=pragma_order):
        # if the pragma was understood and in range we get the value
        # back, while key related ones return 'ok'
        expected = "ok" if pragma_order((pragma, value)) == 100 else str(value)
        if db.pragma(pragma, value) != expected:
            raise ValueError(f"Failed to configure {pragma=}")

    # Check integrity of the database.  If the database is encrypted and
    # the cipher/key information is wrong you will get NotADBError
    # because the file looks like random noise
    try:
        db.pragma("quick_check")
    except NotADBError:
        raise NotADBError(f"Unable to read encrypted meta database. Is the key correct?")