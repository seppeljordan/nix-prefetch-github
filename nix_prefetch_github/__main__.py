import click

from .core import GithubRepository, prefetch_github
from .effect import perform_effects
from .version import VERSION_STRING


def nix_prefetch_github(owner, repo, prefetch=True, rev=None, fetch_submodules=False):
    return perform_effects(
        prefetch_github(
            repository=GithubRepository(owner=owner, name=repo),
            rev=rev,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )
    )


PREFETCH_DEFAULT = True
NIX_DEFAULT = False
FETCH_SUBMODULES_DEFAULT = True
REV_DEFAULT = None


@click.command("nix-prefetch-github")
@click.argument("owner")
@click.argument("repo")
@click.option(
    "--prefetch/--no-prefetch",
    default=PREFETCH_DEFAULT,
    help="Prefetch given repository into nix store",
)
@click.option(
    "--nix/--json",
    is_flag=True,
    help="Format output as Nix expression",
    default=NIX_DEFAULT,
)
@click.option(
    "--fetch-submodules",
    is_flag=FETCH_SUBMODULES_DEFAULT,
    help="Whether to fetch submodules contained in the target repository",
)
@click.option("--rev", default=REV_DEFAULT, type=str)
@click.version_option(version=VERSION_STRING, prog_name="nix-prefetch-github")
def main(
    owner,
    repo,
    prefetch=PREFETCH_DEFAULT,
    nix=NIX_DEFAULT,
    rev=REV_DEFAULT,
    fetch_submodules=FETCH_SUBMODULES_DEFAULT,
):
    prefetched_repository = nix_prefetch_github(
        owner, repo, prefetch, rev, fetch_submodules=fetch_submodules
    )

    if nix:
        output_to_user = prefetched_repository.to_nix_expression()
    else:
        output_to_user = prefetched_repository.to_json_string()

    print(output_to_user, end="")
