"""Provide routines to the public without the need to use the effect library"""

from functools import wraps

from nix_prefetch_github import core

from ..effects import perform_effects
from ..remote_list_factory import RemoteListFactoryImpl
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
            revision_index=core.RevisionIndex(
                remote_list_factory=RemoteListFactoryImpl()
            ),
            repository=core.GithubRepository(owner=owner, name=repo),
            rev=rev,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )
    )


def prefetch_latest_release(repository, prefetch=True, fetch_submodules=False):
    return perform_effects(
        core.prefetch_latest_release(
            url_hasher=UrlHasherImpl(),
            revision_index=core.RevisionIndex(
                remote_list_factory=RemoteListFactoryImpl()
            ),
            repository=repository,
            prefetch=prefetch,
            fetch_submodules=fetch_submodules,
        )
    )


check_repository_is_dirty = make_standalone(core.check_repository_is_dirty)
