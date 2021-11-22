import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional, Tuple

from nix_prefetch_github.templates import output_template

from .core.repository import GithubRepository
from .core.url_hasher import PrefetchOptions

trash_sha256 = "1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv"


class UrlHasherImpl:
    def calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        status_code, output = run_fetch_command(
            repository,
            revision,
            trash_sha256,
            prefetch_options,
        )
        return detect_actual_hash_from_nix_output(output.splitlines())


def run_fetch_command(
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
    )
    with TemporaryDirectory() as temp_dir_name:
        nix_filename = temp_dir_name + "/prefetch-github.nix"
        with open(nix_filename, "w") as f:
            f.write(nix_code_calculate_hash)
        result = run_command(
            command=["nix-build", nix_filename, "--no-out-link"],
            merge_stderr=True,
        )
        return result


def run_command(
    command: List[str],
    cwd: Optional[str] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    merge_stderr: bool = False,
) -> Tuple[int, str]:
    if environment_variables is None:
        environment_variables = dict()
    target_environment = dict(os.environ, **environment_variables)
    stderr = subprocess.STDOUT if merge_stderr else subprocess.PIPE
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=stderr,
        universal_newlines=True,
        cwd=cwd,
        env=target_environment,
    )
    process_stdout, process_stderr = process.communicate()
    if merge_stderr:
        print(process_stdout, file=sys.stderr)
    else:
        print(process_stderr, file=sys.stderr)
    return process.returncode, process_stdout


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
