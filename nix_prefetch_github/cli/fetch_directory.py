import click
from effect import Effect
from effect.do import do

from nix_prefetch_github.core import GetCurrentDirectory, prefetch_directory
from nix_prefetch_github.effects import perform_effects


@click.command("nix-prefetch-github-directory")
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
    def detect_directory_and_prefetch():
        nonlocal directory
        if not directory:
            directory = yield Effect(GetCurrentDirectory())
        return prefetch_directory(
            directory=directory,
            remote=remote,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )

    prefetched_repository = perform_effects(detect_directory_and_prefetch())
    if nix:
        print(prefetched_repository.to_nix_expression())
    else:
        print(prefetched_repository.to_json_string())


if __name__ == "__main__":
    main()
