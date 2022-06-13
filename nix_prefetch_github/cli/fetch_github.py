import sys

from nix_prefetch_github.dependency_injector import DependencyInjector


def main() -> None:
    injector = DependencyInjector()
    controller = injector.get_prefetch_github_repository_controller()
    controller.process_arguments(sys.argv[1:])


if __name__ == "__main__":
    main()
