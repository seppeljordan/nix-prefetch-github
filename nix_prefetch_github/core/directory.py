from effect import Effect
from effect.do import do

from .effects import (
    CheckGitRepoIsDirty,
    DetectGithubRepository,
    DetectRevision,
    ShowWarning,
)
from .prefetch import RevisionIndexFactory, prefetch_github
from .url_hasher import UrlHasher


@do
def prefetch_directory(
    url_hasher: UrlHasher,
    revision_index: RevisionIndexFactory,
    directory,
    remote,
    prefetch=True,
    fetch_submodules=True,
):
    is_repo_dirty = yield check_repository_is_dirty(directory)
    if is_repo_dirty:
        yield Effect(ShowWarning(message=f"Repository at {directory} dirty"))
    repository = yield Effect(
        DetectGithubRepository(directory=directory, remote=remote)
    )
    current_revision = yield Effect(DetectRevision(directory))
    prefetched_repository = yield prefetch_github(
        revision_index_factory=revision_index,
        url_hasher=url_hasher,
        repository=repository,
        prefetch=prefetch,
        fetch_submodules=fetch_submodules,
        rev=current_revision,
    )
    return prefetched_repository


def check_repository_is_dirty(directory):
    return Effect(CheckGitRepoIsDirty(directory=directory))
