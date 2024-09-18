import hashlib

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"

def compact_hash(s: str, n: int) -> str:
    result = []
    digest = int(hashlib.md5(s.encode()).hexdigest(), 16)
    for _ in range(n):
        result.append(alphabet[digest % 36])
        digest //= 36
    return "".join(result)