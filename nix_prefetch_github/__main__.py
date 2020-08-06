import click

from .core import prefetch_github
from .effect import perform_effects
from .version import VERSION_STRING


def nix_prefetch_github(owner, repo, prefetch=True, rev=None, fetch_submodules=False):
    return perform_effects(
        prefetch_github(
            owner=owner,
            repo=repo,
            rev=rev,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )
    )


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
    prefetched_repository = nix_prefetch_github(
        owner, repo, prefetch, rev, fetch_submodules=fetch_submodules
    )

    if nix:
        output_to_user = prefetched_repository.to_nix_expression()
    else:
        output_to_user = prefetched_repository.to_json_string()

    print(output_to_user, end="")
