from dataclasses import dataclass
from typing import Optional

from nix_prefetch_github.interfaces import CommandRunner


@dataclass
class HashConverterImpl:
    command_runner: CommandRunner

    def convert_sha256_to_sri(self, original: str) -> Optional[str]:
        returncode, output = self.command_runner.run_command(
            [
                "nix",
                "--extra-experimental-features",
                "nix-command",
                "hash",
                "to-sri",
                f"sha256:{original}",
            ],
        )
        if not returncode:
            return output.strip()
        return None
