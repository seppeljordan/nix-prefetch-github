"""Provide routines to the public without the need to use the effect library"""

from functools import wraps

from nix_prefetch_github import core

from ..effects import perform_effects
from ..url_hasher import UrlHasherImpl


def make_standalone(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return perform_effects(f(*args, **kwargs))

    return wrapper


def nix_prefetch_github(owner, repo, prefetch=True, rev=None, fetch_submodules=False):
    return perform_effects(
        core.prefetch_github(
            url_hasher=UrlHasherImpl(),
            repository=core.GithubRepository(owner=owner, name=repo),
            rev=rev,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )
    )


check_repository_is_dirty = make_standalone(core.check_repository_is_dirty)
prefetch_latest_release = make_standalone(core.prefetch_latest_release)
