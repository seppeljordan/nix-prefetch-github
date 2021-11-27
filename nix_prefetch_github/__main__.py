import argparse

from .public import nix_prefetch_github
from .version import VERSION_STRING

PREFETCH_DEFAULT = True
NIX_DEFAULT = False
FETCH_SUBMODULES_DEFAULT = True
REV_DEFAULT = None


def main(arguments=None):
    arguments = parse_arguments(arguments)
    if arguments.version:
        print_version_info()
        return None
    prefetched_repository = nix_prefetch_github(
        arguments.owner,
        arguments.repo,
        arguments.rev,
        fetch_submodules=arguments.fetch_submodules,
    )
    if arguments.nix:
        output_to_user = prefetched_repository.to_nix_expression()
    else:
        output_to_user = prefetched_repository.to_json_string()
    print(output_to_user, end="")


def print_version_info() -> None:
    print(f"nix-prefetch-github {VERSION_STRING}")


def parse_arguments(arguments) -> argparse.Namespace:
    parser = argparse.ArgumentParser("nix-prefetch-github")
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument(
        "--fetch-submodules", action="store_true", default=FETCH_SUBMODULES_DEFAULT
    )
    parser.add_argument(
        "--no-fetch-submodules", action="store_false", dest="fetch_submodules"
    )
    parser.add_argument("--rev", default=REV_DEFAULT)
    parser.add_argument("--nix", default=NIX_DEFAULT, action="store_true")
    parser.add_argument("--json", dest="nix", action="store_false")
    parser.add_argument("--version", "-V", action="store_true")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
