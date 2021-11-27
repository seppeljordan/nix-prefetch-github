import json
from dataclasses import dataclass
from typing import Optional, cast

from attr import attrib, attrs
from effect import Effect
from effect.do import do

from nix_prefetch_github.templates import output_template

from .effects import AbortWithErrorMessage, GetRevisionForLatestRelease, TryPrefetch
from .error import AbortWithError
from .hash import is_sha1_hash
from .repository import GithubRepository
from .revision_index import RevisionIndex
from .url_hasher import PrefetchOptions, UrlHasher


def revision_not_found_errormessage(repository: GithubRepository, revision: str):
    return f"Revision {revision} not found for repository {repository.owner}/{repository.name}"


def repository_not_found_error_message(repository: GithubRepository):
    return f"Could not find release for {repository.owner}/{repository.name}"


@dataclass(frozen=True)
class _Prefetcher:
    url_hasher: UrlHasher
    revision_index: RevisionIndex

    @do
    def prefetch_github(
        self,
        repository: GithubRepository,
        prefetch: bool,
        rev,
        prefetch_options: PrefetchOptions,
    ):
        revision = self._detect_revision(repository, rev)
        if revision is None:
            yield Effect(
                AbortWithErrorMessage(
                    message=revision_not_found_errormessage(
                        repository=repository, revision=rev
                    )
                )
            )
            raise AbortWithError()
        return (
            yield self._prefetch_github(
                repository, prefetch, revision, prefetch_options
            )
        )

    @do
    def prefetch_latest_release(
        self,
        repository: GithubRepository,
        prefetch: bool,
        prefetch_options: PrefetchOptions,
    ):
        revision = yield Effect(GetRevisionForLatestRelease(repository=repository))
        if not revision:
            yield Effect(
                AbortWithErrorMessage(repository_not_found_error_message(repository))
            )
            raise AbortWithError()
        return (
            yield self._prefetch_github(
                repository, prefetch, revision, prefetch_options
            )
        )

    @do
    def _prefetch_github(
        self,
        repository: GithubRepository,
        prefetch: bool,
        revision: str,
        prefetch_options: PrefetchOptions,
    ):
        calculated_hash = self._calculate_sha256_sum(
            repository, revision, prefetch_options
        )
        if calculated_hash is None:
            yield Effect(
                AbortWithErrorMessage(
                    message=(
                        "Internal Error: Calculate hash value for sources "
                        f"in github repo {repository.owner}/{repository.name}."
                    )
                )
            )
        if prefetch:
            yield self._prefetch_repository(
                repository, revision, calculated_hash, prefetch_options
            )
        return PrefetchedRepository(
            repository=repository,
            sha256=calculated_hash,
            rev=revision,
            fetch_submodules=prefetch_options.fetch_submodules,
        )

    def _detect_revision(
        self, repository: GithubRepository, revision: Optional[str]
    ) -> Optional[str]:
        actual_rev: Optional[str]
        if isinstance(revision, str) and is_sha1_hash(revision):
            actual_rev = revision
        elif revision is None:
            actual_rev = self.revision_index.get_revision_by_name(repository, "HEAD")
        else:
            actual_rev = self.revision_index.get_revision_by_name(
                repository, cast(str, revision)
            )
        return actual_rev

    def _calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        return self.url_hasher.calculate_sha256_sum(
            repository=repository,
            revision=revision,
            prefetch_options=prefetch_options,
        )

    @do
    def _prefetch_repository(
        self,
        repository: GithubRepository,
        revision: str,
        calculated_hash: str,
        prefetch_options: PrefetchOptions,
    ):
        yield Effect(
            TryPrefetch(
                repository=repository,
                sha256=calculated_hash,
                rev=revision,
                fetch_submodules=prefetch_options.fetch_submodules,
            )
        )


@attrs
class PrefetchedRepository:
    repository = attrib()
    rev = attrib()
    sha256 = attrib()
    fetch_submodules = attrib()

    def to_nix_expression(self):
        return output_template(
            owner=self.repository.owner,
            repo=self.repository.name,
            rev=self.rev,
            sha256=self.sha256,
            fetch_submodules=self.fetch_submodules,
        )

    def to_json_string(self):
        return json.dumps(
            {
                "owner": self.repository.owner,
                "repo": self.repository.name,
                "rev": self.rev,
                "sha256": self.sha256,
                "fetchSubmodules": self.fetch_submodules,
            },
            indent=4,
        )


def prefetch_github(
    url_hasher: UrlHasher,
    revision_index: RevisionIndex,
    repository,
    prefetch=True,
    rev=None,
    fetch_submodules=True,
):
    prefetcher = _Prefetcher(url_hasher, revision_index)
    return prefetcher.prefetch_github(
        repository=repository,
        prefetch=prefetch,
        rev=rev,
        prefetch_options=PrefetchOptions(fetch_submodules=fetch_submodules),
    )


def prefetch_latest_release(
    url_hasher: UrlHasher,
    revision_index: RevisionIndex,
    repository,
    prefetch,
    fetch_submodules,
):
    prefetcher = _Prefetcher(url_hasher, revision_index)
    return prefetcher.prefetch_latest_release(
        repository=repository,
        prefetch=prefetch,
        prefetch_options=PrefetchOptions(fetch_submodules=fetch_submodules),
    )
