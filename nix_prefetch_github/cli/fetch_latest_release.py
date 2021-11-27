import argparse

from nix_prefetch_github.core import GithubRepository
from nix_prefetch_github.public import prefetch_latest_release


def main(args=None):
    arguments = parse_arguments(args)
    prefetched_repository = prefetch_latest_release(
        GithubRepository(owner=arguments.owner, name=arguments.repo),
        fetch_submodules=arguments.fetch_submodules,
    )
    if arguments.nix:
        print(prefetched_repository.to_nix_expression())
    else:
        print(prefetched_repository.to_json_string())


def parse_arguments(arguments) -> argparse.Namespace:
    parser = argparse.ArgumentParser("nix-prefetch-github")
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--fetch-submodules", action="store_true", default=False)
    parser.add_argument(
        "--no-fetch-submodules", action="store_false", dest="fetch_submodules"
    )
    parser.add_argument("--nix", default=False, action="store_true")
    parser.add_argument("--json", dest="nix", action="store_false")
    parser.add_argument("--version", "-V", action="store_true")
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
