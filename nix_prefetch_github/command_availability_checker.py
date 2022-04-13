from dataclasses import dataclass

from nix_prefetch_github.command import CommandRunner


@dataclass
class CommandAvailabilityCheckerImpl:
    command_runner: CommandRunner

    def is_command_available(self, command: str) -> bool:
        try:
            exit_code, _ = self.command_runner.run_command(["which", command])
        except FileNotFoundError:
            return False
        return exit_code == 0
