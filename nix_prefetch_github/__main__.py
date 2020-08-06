import json

import click
from effect import sync_perform
from effect.do import do

from .core import prefetch_github
from .effect import dispatcher
from .templates import output_template
from .version import VERSION_STRING


def to_nix_expression(output_dictionary):
    return output_template.render(
        owner=output_dictionary["owner"],
        repo=output_dictionary["repo"],
        rev=output_dictionary["rev"],
        sha256=output_dictionary["sha256"],
        fetch_submodules="true" if output_dictionary["fetchSubmodules"] else "false",
    )


def nix_prefetch_github(owner, repo, prefetch=True, rev=None, fetch_submodules=False):
    @do
    def main_intent():
        prefetch_results = yield prefetch_github(
            owner, repo, prefetch, rev=rev, fetch_submodules=fetch_submodules
        )
        output_dictionary = {
            "owner": owner,
            "repo": repo,
            "rev": prefetch_results["rev"],
            "sha256": prefetch_results["sha256"],
            "fetchSubmodules": fetch_submodules,
        }

        return output_dictionary

    return sync_perform(dispatcher(), main_intent())


@click.command("nix-prefetch-github")
@click.argument("owner")
@click.argument("repo")
@click.option(
    "--prefetch/--no-prefetch",
    default=True,
    help="Prefetch given repository into nix store",
)
@click.option("--nix", is_flag=True, help="Format output as Nix expression")
@click.option(
    "--fetch-submodules",
    is_flag=True,
    help="Whether to fetch submodules contained in the target repository",
)
@click.option("--rev", default=None, type=str)
@click.version_option(version=VERSION_STRING, prog_name="nix-prefetch-github")
def _main(owner, repo, prefetch, nix, rev, fetch_submodules):
    output_dictionary = nix_prefetch_github(
        owner, repo, prefetch, rev, fetch_submodules=fetch_submodules
    )

    if nix:
        output_to_user = to_nix_expression(output_dictionary)
    else:
        output_to_user = json.dumps(output_dictionary, indent=4)

    print(output_to_user, end="")
