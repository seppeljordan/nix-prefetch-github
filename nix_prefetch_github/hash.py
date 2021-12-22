import re


def is_sha1_hash(text: str) -> bool:
    return bool(re.match(r"^[0-9a-f]{40}$", text))
