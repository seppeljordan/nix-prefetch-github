import json
import os
import re
import subprocess
from tempfile import TemporaryDirectory

import click
import jinja2
import requests

HERE = os.path.dirname(__file__)


def cmd(command):
    process_return = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    return process_return.returncode, process_return.stdout


def get_latest_commit_from_github(owner, repo):
    url_template = 'https://api.github.com/repos/{owner}/{repo}/commits/master'
    request_url = url_template.format(
        owner=owner,
        repo=repo,
    )
    response = requests.get(request_url)
    return response.json()['sha']


def prefetch_github(owner, repo, hash_only=False, rev=None):
    def select_hash_from_match(match):
        hash_untrimmed = match.group(1) or match.group(2)
        if hash_untrimmed:
            return hash_untrimmed[1:-1]
        else:
            return None

    templates_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(HERE + '/templates'),
    )
    template = templates_env.get_template('prefetch-github.nix.j2')

    def do_prefetch(sha256, rev):
        nix_code_calculate_hash = template.render(
            owner=owner,
            repo=repo,
            rev=rev,
            sha256=sha256,
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

    actual_rev = rev or get_latest_commit_from_github(owner, repo)
    trash_sha256 = '1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv'
    output=do_prefetch(sha256=trash_sha256, rev=actual_rev)['output']
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
        do_prefetch(sha256=calculated_hash, rev=actual_rev)
    return {
        'rev': actual_rev,
        'sha256': calculated_hash,
    }


@click.command('nix-prefetch-github')
@click.argument('owner')
@click.argument('repo')
@click.option('--hash-only/--no-hash-only', default=False)
@click.option('--rev', default=None, type=str)
def main(owner, repo, hash_only, rev):
    repo_data = prefetch_github(
        owner, repo, hash_only, rev=rev
    )
    print(
        json.dumps(
            {
                "owner": owner,
                "repo": repo,
                "rev": repo_data['rev'],
                "sha256": repo_data['sha256'],
            },
            indent=4,
        )
    )
