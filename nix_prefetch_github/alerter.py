from dataclasses import dataclass
from logging import Logger

from nix_prefetch_github.interfaces import PrefetchOptions


@dataclass
class CliAlerterImpl:
    logger: Logger

    def alert_user_about_unsafe_prefetch_options(
        self, prefetch_options: PrefetchOptions
    ) -> None:
        if prefetch_options.deep_clone:
            self._emit_option_warning("--deep-clone")
        if prefetch_options.leave_dot_git:
            self._emit_option_warning("--leave-dot-git")

    def _emit_option_warning(self, option: str) -> None:
        issue = "https://github.com/NixOS/nixpkgs/issues/8567"
        self.logger.warning(
            "%s was used. The resulting fetchFromGitHub directive might be non deterministic. Check %s for more information",
            option,
            issue,
        )
