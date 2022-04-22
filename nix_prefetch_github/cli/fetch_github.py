import sys
from typing import List, Optional

from nix_prefetch_github.dependency_injector import DependencyInjector

PREFETCH_DEFAULT = True
NIX_DEFAULT = False
FETCH_SUBMODULES_DEFAULT = True
REV_DEFAULT = None


def main(argv: Optional[List[str]] = None) -> None:
    injector = DependencyInjector()
    controller = injector.get_prefetch_github_repository_controller()
    controller.process_arguments(sys.argv[1:])


if __name__ == "__main__":
    main()
