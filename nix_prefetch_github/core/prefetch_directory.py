from effect import Effect
from effect.do import do

from .effects import DetectGithubRepository, DetectRevision, GetCurrentDirectory
from .prefetch import prefetch_github


@do
def prefetch_directory(
    directory, remote, prefetch=True, fetch_submodules=True, nix=False
):
    if not directory:
        directory = yield Effect(GetCurrentDirectory())
    github_repository = yield Effect(
        DetectGithubRepository(directory=directory, remote=remote)
    )
    current_revision = yield Effect(DetectRevision(directory))
    prefetched_repository = yield prefetch_github(
        owner=github_repository.owner,
        repo=github_repository.name,
        prefetch=prefetch,
        fetch_submodules=fetch_submodules,
        rev=current_revision,
    )
    if nix:
        print(prefetched_repository.to_nix_expression())
    else:
        print(prefetched_repository.to_json_string())
