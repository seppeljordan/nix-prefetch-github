import argparse

from effect import Effect
from effect.do import do

from ..core import GetCurrentDirectory, prefetch_directory
from ..dependency_injector import DependencyInjector
from ..effects import perform_effects


def main(args=None):
    dependency_injector = DependencyInjector()
    arguments = parser_arguments(args)

    @do
    def detect_directory_and_prefetch():
        if not arguments.directory:
            directory = yield Effect(GetCurrentDirectory())
        return prefetch_directory(
            url_hasher=dependency_injector.get_url_hasher(),
            revision_index_factory=dependency_injector.get_revision_index_factory(),
            directory=directory,
            remote=arguments.remote,
            prefetch=arguments.prefetch,
            fetch_submodules=arguments.fetch_submodules,
        )

    prefetched_repository = perform_effects(detect_directory_and_prefetch())
    if arguments.nix:
        print(prefetched_repository.to_nix_expression())
    else:
        print(prefetched_repository.to_json_string())


def parser_arguments(arguments=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory")
    parser.add_argument(
        "--nix",
        action="store_true",
        default=False,
        help="Format output as Nix expression",
    )
    parser.add_argument("--json", dest="nix", action="store_false")
    parser.add_argument("--remote", default="origin")
    parser.add_argument(
        "--prefetch",
        default=False,
        action="store_true",
        help="Prefetch given repository into nix store",
    )
    parser.add_argument("--no-prefetch", dest="prefetch", action="store_false")
    parser.add_argument(
        "--fetch-submodules",
        default=False,
        action="store_true",
        help="Whether to fetch submodules contained in the target repository",
    )
    return parser.parse_args(arguments)


if __name__ == "__main__":
    main()
