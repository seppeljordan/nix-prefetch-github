import click

from .core import prefetch_directory
from .effect import perform_effects


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
    perform_effects(
        prefetch_directory(
            directory=directory,
            remote=remote,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
            nix=nix,
        )
    )


if __name__ == "__main__":
    main()
