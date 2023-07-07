import re
from dataclasses import dataclass
from logging import Logger
from tempfile import TemporaryDirectory
from typing import List, Optional, Tuple

from nix_prefetch_github.interfaces import (
    CommandRunner,
    GithubRepository,
    HashConverter,
    PrefetchOptions,
)
from nix_prefetch_github.templates import output_template

trash_sha256 = ""


@dataclass(frozen=True)
class NixBuildUrlHasherImpl:
    command_runner: CommandRunner
    logger: Logger
    hash_converter: HashConverter

    def calculate_hash_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        status_code, output = self.run_fetch_command(
            repository,
            revision,
            trash_sha256,
            prefetch_options,
        )
        sha256 = detect_actual_hash_from_nix_output(output.splitlines())
        if sha256 is None:
            return None
        return self.hash_converter.convert_sha256_to_sri(sha256)

    def run_fetch_command(
        self,
        repository: GithubRepository,
        rev: str,
        sha256: str,
        prefetch_options: PrefetchOptions,
    ) -> Tuple[int, str]:
        nix_code_calculate_hash = output_template(
            owner=repository.owner,
            repo=repository.name,
            rev=rev,
            sha256=sha256,
            fetch_submodules=prefetch_options.fetch_submodules,
            leave_dot_git=prefetch_options.leave_dot_git,
            deep_clone=prefetch_options.deep_clone,
        )
        self.logger.info("Evaluating nix expression \n%s", nix_code_calculate_hash)
        with TemporaryDirectory() as temp_dir_name:
            nix_filename = temp_dir_name + "/prefetch-github.nix"
            with open(nix_filename, "w") as f:
                f.write(nix_code_calculate_hash)
            result = self.command_runner.run_command(
                command=["nix-build", nix_filename, "--no-out-link"],
                merge_stderr=True,
            )
            return result


def detect_actual_hash_from_nix_output(lines: List[str]) -> Optional[str]:
    nix_1_x_regexp = r"output path .* has .* hash '(?P<hash>[a-z0-9]{52})' when .*"
    nix_2_0_regexp = r"fixed\-output derivation produced path .* with sha256 hash '(?P<hash>[a-z0-9]{52})' instead of the expected hash .*"
    nix_2_2_regexp = r"  got: +sha256:(?P<hash>[a-z0-9]{52})"
    nix_2_4_regexp = r" +got: +(sha256-)?(?P<hash>.+)"

    def try_extract_hash(line: str) -> Optional[str]:
        possible_patterns = [
            re.compile(pattern)
            for pattern in (
                nix_1_x_regexp,
                nix_2_0_regexp,
                nix_2_2_regexp,
                nix_2_4_regexp,
            )
        ]
        for pattern in possible_patterns:
            result: Optional[re.Match] = re.match(pattern, line)
            if result:
                return result.group("hash")
        return None

    for line in lines:
        possible_result = try_extract_hash(line)
        if possible_result:
            return possible_result
    return None
