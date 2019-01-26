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

HERE = os.path.dirname(__file__)
trash_sha256 = '1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv'
templates_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(HERE + '/templates'),
)
template = templates_env.get_template('prefetch-github.nix.j2')


class DownloadException(Exception):
    pass


@attr.s
class TryPrefetch(object):
    owner = attr.ib()
    repo = attr.ib()
    sha256 = attr.ib()
    rev = attr.ib()


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
        return {
            'returncode': returncode,
            'output': output
        }


@attr.s
class PrefetchGit(object):
    url = attr.ib()


@sync_performer
def prefetch_git_performer(dispatcher, prefetch_git):
    return_code, stdout = cmd(
        ["nix-prefetch-git", prefetch_git.url],
        merge_stderr=False
    )
    return json.loads(stdout)


@attrs
class GetCommitHashForName:
    owner = attrib()
    repo = attrib()
    rev = attrib()


@sync_performer
def get_commit_hash_for_name_performer(_, intent):
    repository_url = 'https://github.com/{owner}/{repo}.git'.format(
        owner=intent.owner,
        repo=intent.repo,
    )
    return_code, output = cmd(
        command=[
            'git',
            'ls-remote',
            '--heads',
            '--tags',
            repository_url,
        ] + ([intent.rev] if intent.rev else []),
    )
    if return_code:
       return None
    else:
        return output.split('\t')[0]


def dispatcher():
    prefetch_dispatcher = TypeDispatcher({
        TryPrefetch: try_prefetch_performer,
        PrefetchGit: prefetch_git_performer,
        GetCommitHashForName: get_commit_hash_for_name_performer,
    })
    return ComposedDispatcher([
        base_dispatcher,
        prefetch_dispatcher
    ])


@do
def prefetch_github(owner, repo, hash_only=False, rev=None):
    def select_hash_from_match(match):
        hash_untrimmed = match.group(1) or match.group(2)
        return hash_untrimmed[1:-1]

    if isinstance(rev, str) and is_sha1_hash(rev):
        actual_rev = rev
    else:
        actual_rev = yield Effect(GetCommitHashForName(
            owner=owner,
            repo=repo,
            rev=rev,
        ))

    output=(yield Effect(TryPrefetch(
        owner=owner,
        repo=repo,
        sha256=trash_sha256,
        rev=actual_rev
    )))['output']
    r = re.compile(
        "|".join(
            ["output path .* has .* hash (.*) when .*",
             "fixed\-output derivation produced path .* with sha256 hash (.*) instead of the expected hash .*", # flake8: noqa: E501
            ]
        )
    )
    calculated_hash = None
    for line in output.splitlines():
        re_match = r.match(line)
        if not re_match:
            continue
        calculated_hash = select_hash_from_match(re_match)
        break
    if not calculated_hash:
        raise click.ClickException(
            (
                'Internal Error: Calculate hash value for sources '
                'in github repo {owner}/{repo}.\n\noutput was: {output}'
            ).format(owner=owner, repo=repo, output=output)
        )
    if not hash_only:
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


def nix_prefetch_github(owner, repo, hash_only=True, rev=None):

    @do
    def main_intent():
        prefetch_results = yield prefetch_github(
            owner,
            repo,
            hash_only,
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
@click.option('--hash-only/--no-hash-only', default=False)
@click.option('--rev', default=None, type=str)
def _main(owner, repo, hash_only, rev):
    output_dictionary = nix_prefetch_github(owner, repo, hash_only, rev)
    output_to_user = json.dumps(
        output_dictionary,
        indent=4,
    )

    print(output_to_user)
