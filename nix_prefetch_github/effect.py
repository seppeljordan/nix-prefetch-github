import re
from tempfile import TemporaryDirectory

import effect.io
from effect import ComposedDispatcher, Effect, TypeDispatcher, sync_performer
from effect.do import do

from .core import AbortWithErrorMessage, CalculateSha256Sum, GetListRemote, TryPrefetch
from .error import abort_with_error_message_performer
from .io import cmd
from .list_remote import ListRemote
from .templates import output_template

trash_sha256 = "1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv"


base_dispatcher = effect.ComposedDispatcher(
    [effect.base_dispatcher, effect.io.stdio_dispatcher]
)


def make_effect_dispatcher(mapping):
    return effect.TypeDispatcher(
        {
            the_type: sync_performer(lambda _, intent: perform_effect(intent))
            for the_type, perform_effect in mapping.items()
        }
    )


def dispatcher():
    prefetch_dispatcher = TypeDispatcher(
        {
            TryPrefetch: try_prefetch_performer,
            GetListRemote: get_list_remote_performer,
            AbortWithErrorMessage: abort_with_error_message_performer,
        }
    )
    composed_performers = make_effect_dispatcher(
        {CalculateSha256Sum: calculate_sha256_sum}
    )
    return ComposedDispatcher(
        [base_dispatcher, prefetch_dispatcher, composed_performers]
    )


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
        returncode, output = cmd(["nix-build", nix_filename])
        return returncode, output


@sync_performer
def get_list_remote_performer(_, intent):
    repository_url = "https://github.com/{owner}/{repo}.git".format(
        owner=intent.owner, repo=intent.repo
    )
    _, stdout = cmd(["git", "ls-remote", "--symref", repository_url])
    return ListRemote.from_git_ls_remote_output(stdout)


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
