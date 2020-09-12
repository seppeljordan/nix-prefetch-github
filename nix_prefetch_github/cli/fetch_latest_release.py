import click

from nix_prefetch_github.core import GithubRepository
from nix_prefetch_github.public import prefetch_latest_release


@click.command("nix-prefetch-github-latest-release")
@click.argument("owner")
@click.argument("repo")
@click.option("--nix", is_flag=True, help="Format output as Nix expression")
@click.option(
    "--prefetch/--no-prefetch",
    default=True,
    help="Prefetch given repository into nix store",
)
@click.option(
    "--fetch-submodules",
    is_flag=True,
    help="Whether to fetch submodules contained in the target repository",
)
def main(owner, repo, nix, prefetch, fetch_submodules):
    prefetched_repository = prefetch_latest_release(
        GithubRepository(owner=owner, name=repo),
        prefetch=prefetch,
        fetch_submodules=fetch_submodules,
    )
    if nix:
        print(prefetched_repository.to_nix_expression())
    else:
        print(prefetched_repository.to_json_string())


if __name__ == "__main__":
    main()
