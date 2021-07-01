import json
import os
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Dict, Optional
from urllib.error import HTTPError
from urllib.request import urlopen

import effect.io
from attr import attrib, attrs
from effect import (
    ComposedDispatcher,
    Effect,
    TypeDispatcher,
    sync_perform,
    sync_performer,
)
from effect.do import do

from .core import (
    AbortWithErrorMessage,
    CalculateSha256Sum,
    CheckGitRepoIsDirty,
    DetectGithubRepository,
    DetectRevision,
    GetCurrentDirectory,
    GetListRemote,
    GetRevisionForLatestRelease,
    GithubRepository,
    ShowWarning,
    TryPrefetch,
)
from .core.list_remote import ListRemote
from .templates import output_template

trash_sha256 = "1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv"


base_dispatcher = effect.ComposedDispatcher(
    [effect.base_dispatcher, effect.io.stdio_dispatcher]
)


def make_effect_dispatcher(mapping):
    def make_performer(effect):
        def _performer(dispatcher, intent):
            return sync_perform(dispatcher, effect(intent))

        return _performer

    return effect.TypeDispatcher(
        {
            the_type: sync_performer(make_performer(perform_effect))
            for the_type, perform_effect in mapping.items()
        }
    )


def dispatcher():
    prefetch_dispatcher = TypeDispatcher(
        {
            AbortWithErrorMessage: abort_with_error_message_performer,
            ExecuteCommand: execute_command_performer,
            GetCurrentDirectory: get_current_directory_performer,
            ShowWarning: show_warning_performer,
        }
    )
    composed_performers = make_effect_dispatcher(
        {
            GetRevisionForLatestRelease: get_revision_for_latest_release_performer,
            CalculateSha256Sum: calculate_sha256_sum,
            GetListRemote: get_list_remote_performer,
            TryPrefetch: try_prefetch_performer,
            DetectGithubRepository: detect_github_repository,
            DetectRevision: detect_revision,
            CheckGitRepoIsDirty: check_git_repo_is_dirty_performer,
        }
    )
    return ComposedDispatcher(
        [base_dispatcher, prefetch_dispatcher, composed_performers]
    )


@do
def detect_github_repository(intent):
    returncode, stdout = yield Effect(
        ExecuteCommand(
            command=["git", "remote", "get-url", intent.remote], cwd=intent.directory
        )
    )
    match = re.match("(git@github.com:|https://github.com/)(.+)/(.+).git", stdout)
    if not match:
        yield Effect(
            AbortWithErrorMessage(
                message=f"Remote '{intent.remote}' is not a link to a github repository"
            )
        )
    else:
        owner = match.group(2)
        name = match.group(3)
        return GithubRepository(
            name=name,
            owner=owner,
        )


@do
def detect_revision(intent):
    returncode, stdout = yield Effect(
        ExecuteCommand(command=["git", "rev-parse", "HEAD"], cwd=intent.directory)
    )
    return stdout[:-1]


@sync_performer
def get_current_directory_performer(_, _intent):
    return os.getcwd()


@do
def try_prefetch_performer(try_prefetch):
    nix_code_calculate_hash = output_template(
        owner=try_prefetch.repository.owner,
        repo=try_prefetch.repository.name,
        rev=try_prefetch.rev,
        sha256=try_prefetch.sha256,
        fetch_submodules=try_prefetch.fetch_submodules,
    )
    with TemporaryDirectory() as temp_dir_name:
        nix_filename = temp_dir_name + "/prefetch-github.nix"
        with open(nix_filename, "w") as f:
            f.write(nix_code_calculate_hash)
        result = yield Effect(
            ExecuteCommand(
                command=["nix-build", nix_filename, "--no-out-link"],
                merge_stderr=True,
            )
        )
        return result


@do
def get_list_remote_performer(intent):
    repository_url = intent.repository.url()
    command_effect = ExecuteCommand(
        command=["git", "ls-remote", "--symref", repository_url],
        environment_variables={"GIT_ASKPASS": "", "GIT_TERMINAL_PROMPT": "0"},
    )

    returncode, stdout = yield Effect(command_effect)
    if not returncode:
        return ListRemote.from_git_ls_remote_output(stdout)
    else:
        yield Effect(
            AbortWithErrorMessage(
                f"{command_effect} failed with returncode {returncode}."
            )
        )


@do
def calculate_sha256_sum(intent):
    return_code, nix_output = yield Effect(
        TryPrefetch(
            repository=intent.repository,
            sha256=trash_sha256,
            rev=intent.revision,
            fetch_submodules=intent.fetch_submodules,
        )
    )
    return detect_actual_hash_from_nix_output(nix_output.splitlines())


def detect_actual_hash_from_nix_output(lines):
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


@sync_performer
def execute_command_performer(_, intent):
    target_environment = dict(os.environ, **intent.environment_variables)
    stderr = subprocess.STDOUT if intent.merge_stderr else subprocess.PIPE
    process = subprocess.Popen(
        intent.command,
        stdout=subprocess.PIPE,
        stderr=stderr,
        universal_newlines=True,
        cwd=intent.cwd,
        env=target_environment,
    )
    process_stdout, process_stderr = process.communicate()
    if intent.merge_stderr:
        print(process_stdout, file=sys.stderr)
    else:
        print(process_stderr, file=sys.stderr)
    return process.returncode, process_stdout


def perform_effects(effects):
    return sync_perform(dispatcher(), effects)


@sync_performer
def abort_with_error_message_performer(_, intent):
    print(intent.message, file=sys.stderr)
    exit(1)


@sync_performer
def show_warning_performer(_, intent):
    print(f"WARNING: {intent.message}", file=sys.stderr)


@do
def check_git_repo_is_dirty_performer(intent):
    returncode, _ = yield Effect(
        ExecuteCommand(
            command=["git", "diff", "HEAD", "--quiet"],
            cwd=intent.directory,
        )
    )
    if returncode == 128:
        raise Exception(
            f"Repository at {intent.directory} does not contain any commits"
        )
    return returncode != 0


@do
def get_revision_for_latest_release_performer(intent):
    url = f"https://api.github.com/repos/{intent.repository.owner}/{intent.repository.name}/releases/latest"
    try:
        with urlopen(url) as response:
            encoding = response.info().get_content_charset("utf-8")
            content_data = response.read()
    except HTTPError:
        return None
    content_json = json.loads(content_data.decode(encoding))
    tag = content_json["tag_name"]
    remote_list = yield Effect(GetListRemote(intent.repository))
    return remote_list.tag(tag)


@attrs
class ExecuteCommand:
    command = attrib()
    cwd = attrib(default=None)
    merge_stderr = attrib(default=False)
    environment_variables: Dict[str, Optional[str]] = attrib(default={})
