import os
import re
import sys
from tempfile import TemporaryDirectory

import effect.io
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
    DetectGithubRepository,
    DetectRevision,
    ExecuteCommand,
    GetCurrentDirectory,
    GetListRemote,
    GithubRepository,
    TryPrefetch,
)
from .io import cmd
from .list_remote import ListRemote
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
            TryPrefetch: try_prefetch_performer,
            GetListRemote: get_list_remote_performer,
            AbortWithErrorMessage: abort_with_error_message_performer,
            ExecuteCommand: execute_command_performer,
            GetCurrentDirectory: get_current_directory_performer,
        }
    )
    composed_performers = make_effect_dispatcher(
        {
            CalculateSha256Sum: calculate_sha256_sum,
            DetectGithubRepository: detect_github_repository,
            DetectRevision: detect_revision,
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
    owner = match.group(2)
    name = match.group(3)
    return GithubRepository(name=name, owner=owner,)


@do
def detect_revision(intent):
    returncode, stdout = yield Effect(
        ExecuteCommand(command=["git", "rev-parse", "HEAD"], cwd=intent.directory)
    )
    return stdout[:-1]


@sync_performer
def get_current_directory_performer(_, _intent):
    return os.getcwd()


@sync_performer
def try_prefetch_performer(dispatcher, try_prefetch):
    nix_code_calculate_hash = output_template.render(
        owner=try_prefetch.owner,
        repo=try_prefetch.repo,
        rev=try_prefetch.rev,
        sha256=try_prefetch.sha256,
        fetch_submodules="true" if try_prefetch.fetch_submodules else "false",
    )
    with TemporaryDirectory() as temp_dir_name:
        nix_filename = temp_dir_name + "/prefetch-github.nix"
        with open(nix_filename, "w") as f:
            f.write(nix_code_calculate_hash)
        returncode, output = cmd(["nix-build", nix_filename, "--no-out-link"])
        return returncode, output


@sync_performer
def get_list_remote_performer(_, intent):
    repository_url = "https://github.com/{owner}/{repo}.git".format(
        owner=intent.owner, repo=intent.repo
    )
    returncode, stdout = cmd(
        ["git", "ls-remote", "--symref", repository_url],
        environment_variables={"GIT_ASKPASS": "", "GIT_TERMINAL_PROMPT": "0"},
    )
    if not returncode:
        return ListRemote.from_git_ls_remote_output(stdout)
    else:
        return None


@do
def calculate_sha256_sum(intent):
    return_code, nix_output = yield Effect(
        TryPrefetch(
            owner=intent.owner,
            repo=intent.repo,
            sha256=trash_sha256,
            rev=intent.revision,
            fetch_submodules=intent.fetch_submodules,
        )
    )
    return detect_actual_hash_from_nix_output(nix_output.splitlines())


def detect_actual_hash_from_nix_output(lines):
    def select_hash_from_match(match):
        return match.group(1) or match.group(2) or match.group(3) or match.group(4)

    nix_1_x_regexp = r"output path .* has .* hash '([a-z0-9]{52})' when .*"
    nix_2_0_regexp = r"fixed\-output derivation produced path .* with sha256 hash '([a-z0-9]{52})' instead of the expected hash .*"  # flake8: noqa: E501
    nix_2_2_regexp = r"  got: +sha256:([a-z0-9]{52})"
    nix_2_4_regexp = r"  got:    (.*)"
    regular_expression = re.compile(
        "|".join([nix_1_x_regexp, nix_2_0_regexp, nix_2_2_regexp, nix_2_4_regexp])
    )
    for line in lines:
        re_match = regular_expression.match(line)
        if re_match:
            return select_hash_from_match(re_match)


@sync_performer
def execute_command_performer(_, intent):
    return cmd(intent.command, cwd=intent.cwd)


def perform_effects(effects):
    return sync_perform(dispatcher(), effects)


@sync_performer
def abort_with_error_message_performer(_, intent):
    print(intent.message, file=sys.stderr)
    exit(1)
