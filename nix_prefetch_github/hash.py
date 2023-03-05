from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class SriHash:
    hash_function: str
    digest: str
    options: List[str]

    @classmethod
    def from_text(cls, text: str) -> SriHash:
        hash_function, remainder = text.split("-", maxsplit=1)
        digest_and_options = remainder.split("?")
        digest = digest_and_options[0]
        return cls(
            hash_function=hash_function,
            digest=digest,
            options=digest_and_options[1:],
        )

    def __str__(self) -> str:
        options = ["?" + option for option in self.options]
        return f"{self.hash_function}-{self.digest}" + "".join(options)


def is_sha1_hash(text: str) -> bool:
    return bool(re.match(r"^[0-9a-f]{40}$", text))
