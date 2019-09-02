import json
import os
import re
import subprocess
from tempfile import TemporaryDirectory

import attr
import click
import jinja2
from attr import attrib, attrs
from effect import (ComposedDispatcher, Constant, Effect, TypeDispatcher,
                    sync_perform, sync_performer)
from effect.do import do
from effect.io import Display
from nix_prefetch_github.effect import base_dispatcher
from nix_prefetch_github.io import cmd
from nix_prefetch_github.list_remote import ListRemote

HERE = os.path.dirname(__file__)
trash_sha256 = '1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv'
templates_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(HERE + '/templates'),
)
template = templates_env.get_template('prefetch-github.nix.j2')
output_template = templates_env.get_template('nix-output.j2')
with open(os.path.join(HERE, 'VERSION')) as f:
    VERSION_STRING = f.read()


@attrs
class TryPrefetch(object):
    owner = attr.ib()
    repo = attr.ib()
    sha256 = attr.ib()
    rev = attr.ib()


def to_nix_expression(output_dictionary):
    return output_template.render(
        owner=output_dictionary['owner'],
        repo=output_dictionary['repo'],
        rev=output_dictionary['rev'],
        sha256=output_dictionary['sha256'],
    )


def is_sha1_hash(text):
    return re.match(r'^[0-9a-f]{40}$', text)


@sync_performer
def try_prefetch_performer(dispatcher, try_prefetch):
    nix_code_calculate_hash = template.render(
        owner=try_prefetch.owner,
        repo=try_prefetch.repo,
        rev=try_prefetch.rev,
        sha256=try_prefetch.sha256,
    )
    with TemporaryDirectory() as temp_dir_name:
        nix_filename = temp_dir_name + '/prefetch-github.nix'
        with open(nix_filename, 'w') as f:
            f.write(nix_code_calculate_hash)
        returncode, output = cmd(['nix-build', nix_filename])
        return returncode, output


@attrs
class CalculateSha256Sum:
    owner = attrib()
    repo = attrib()
    revision = attrib()


@do
def calculate_sha256_sum(intent):
    return_code, nix_output = yield Effect(TryPrefetch(
        owner=intent.owner,
        repo=intent.repo,
        sha256=trash_sha256,
        rev=intent.revision,
    ))
    return detect_actual_hash_from_nix_output(nix_output.splitlines())


@attrs
class GetListRemote:
    owner = attrib()
    repo = attrib()


@sync_performer
def get_list_remote_performer(_, intent):
    repository_url = "https://github.com/{owner}/{repo}.git".format(
        owner=intent.owner,
        repo=intent.repo,
    )
    _, stdout = cmd([
        'git',
        'ls-remote',
        '--symref',
        repository_url,
    ])
    return ListRemote.from_git_ls_remote_output(stdout)


def dispatcher():
    prefetch_dispatcher = TypeDispatcher({
        TryPrefetch: try_prefetch_performer,
        CalculateSha256Sum: sync_performer(
            lambda _, intent: calculate_sha256_sum(intent)
        ),
        GetListRemote: get_list_remote_performer,
    })
    return ComposedDispatcher([
        base_dispatcher,
        prefetch_dispatcher
    ])


def detect_actual_hash_from_nix_output(lines):
    def select_hash_from_match(match):
        return match.group(1) or match.group(2) or match.group(3)

    nix_1_x_regexp = r"output path .* has .* hash '([a-z0-9]{52})' when .*"
    nix_2_0_regexp = r"fixed\-output derivation produced path .* with sha256 hash '([a-z0-9]{52})' instead of the expected hash .*"  # flake8: noqa: E501
    nix_2_2_regexp = r"  got: +sha256:([a-z0-9]{52})"
    regular_expression = re.compile('|'.join([
        nix_1_x_regexp,
        nix_2_0_regexp,
        nix_2_2_regexp,
    ]))
    for line in lines:
        re_match = regular_expression.match(line)
        if re_match:
            return select_hash_from_match(re_match)

@do
def prefetch_github(owner, repo, prefetch=True, rev=None):
    if isinstance(rev, str) and is_sha1_hash(rev):
        actual_rev = rev
    else:
        list_remote = yield Effect(GetListRemote(
            owner=owner,
            repo=repo,
        ))
        if rev is None:
            actual_rev = list_remote.branch(list_remote.symref('HEAD'))
        else:
            actual_rev = list_remote.branch(rev) or list_remote.tag(rev)
            if actual_rev is None:
                raise click.ClickException(
                    f'Could not find remote branch or tag `{rev}`'
                )

    calculated_hash = (yield Effect(CalculateSha256Sum(
        owner=owner,
        repo=repo,
        revision=actual_rev
    )))
    if not calculated_hash:
        raise click.ClickException(
            (
                'Internal Error: Calculate hash value for sources '
                'in github repo {owner}/{repo}.\n\noutput was: {output}'
            ).format(owner=owner, repo=repo, output=output)
        )
    if prefetch:
        yield Effect(TryPrefetch(
            owner=owner,
            repo=repo,
            sha256=calculated_hash,
            rev=actual_rev
        ))
    return Effect(Constant({
        'rev': actual_rev,
        'sha256': calculated_hash,
    }))


def nix_prefetch_github(owner, repo, prefetch=True, rev=None):

    @do
    def main_intent():
        prefetch_results = yield prefetch_github(
            owner,
            repo,
            prefetch,
            rev=rev
        )
        output_dictionary = {
                "owner": owner,
                "repo": repo,
                "rev": prefetch_results['rev'],
                "sha256": prefetch_results['sha256'],
            }

        return output_dictionary

    return sync_perform(dispatcher(), main_intent())


@click.command('nix-prefetch-github')
@click.argument('owner')
@click.argument('repo')
@click.option(
    '--prefetch/--no-prefetch',
    default=True,
    help="Prefetch given repository into nix store",
)
@click.option('--nix', is_flag=True, help="Format output as Nix expression")
@click.option('--rev', default=None, type=str)
@click.version_option(version=VERSION_STRING, prog_name='nix-prefetch-github')
def _main(owner, repo, prefetch, nix, rev):
    output_dictionary = nix_prefetch_github(owner, repo, prefetch, rev)

    if nix:
        output_to_user = to_nix_expression(output_dictionary)
    else:
        output_to_user = json.dumps(
            output_dictionary,
            indent=4,
        )

    print(output_to_user, end='')
