import click
from effect.do import do

from .core import (
    DetectGithubRepository,
    DetectRevision,
    GetCurrentDirectory,
    prefetch_github,
)
from .effect import Effect, perform_effects


@click.command("nix-prefetch-github-local")
@click.option("--directory", default=None)
@click.option("--nix", is_flag=True, help="Format output as Nix expression")
@click.option(
    "--prefetch/--no-prefetch",
    default=True,
    help="Prefetch given repository into nix store",
)
@click.option("--remote", default="origin")
@click.option(
    "--fetch-submodules",
    is_flag=True,
    help="Whether to fetch submodules contained in the target repository",
)
def main(directory, nix, prefetch, fetch_submodules, remote):
    @do
    def _main_intent():
        nonlocal directory
        if not directory:
            directory = yield Effect(GetCurrentDirectory())
        github_repository = yield Effect(
            DetectGithubRepository(directory=directory, remote=remote)
        )
        current_revision = yield Effect(DetectRevision(directory))
        prefetched_repository = yield prefetch_github(
            owner=github_repository.owner,
            repo=github_repository.name,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
            rev=current_revision,
        )
        if nix:
            print(prefetched_repository.to_nix_expression())
        else:
            print(prefetched_repository.to_json_string())

    perform_effects(_main_intent())


if __name__ == "__main__":
    main()
