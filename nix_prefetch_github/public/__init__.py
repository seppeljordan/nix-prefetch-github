"""Provide routines to the public without the need to use the effect library"""

from functools import wraps
from typing import cast

from nix_prefetch_github import core

from ..dependency_injector import DependencyInjector
from ..effects import perform_effects

_injector = None


def get_injector() -> DependencyInjector:
    global _injector
    if _injector is None:
        _injector = DependencyInjector()
    return cast(DependencyInjector, _injector)


def make_standalone(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return perform_effects(f(*args, **kwargs))

    return wrapper


def nix_prefetch_github(owner, repo, prefetch=True, rev=None, fetch_submodules=False):
    injector = get_injector()
    return perform_effects(
        core.prefetch_github(
            url_hasher=injector.get_url_hasher(),
            revision_index_factory=injector.get_revision_index_factory(),
            repository=core.GithubRepository(owner=owner, name=repo),
            rev=rev,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )
    )


def prefetch_latest_release(repository, prefetch=True, fetch_submodules=False):
    injector = get_injector()
    return perform_effects(
        core.prefetch_latest_release(
            url_hasher=injector.get_url_hasher(),
            revision_index_factory=injector.get_revision_index_factory(),
            repository=repository,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )
    )


check_repository_is_dirty = make_standalone(core.check_repository_is_dirty)
