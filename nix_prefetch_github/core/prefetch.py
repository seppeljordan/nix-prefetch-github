from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional, Protocol, cast

from effect import Effect
from effect.do import do

from nix_prefetch_github.templates import output_template

from .effects import AbortWithErrorMessage, GetRevisionForLatestRelease
from .error import AbortWithError
from .hash import is_sha1_hash
from .repository import GithubRepository
from .revision_index import RevisionIndex
from .url_hasher import PrefetchOptions, UrlHasher


def revision_not_found_errormessage(
    repository: GithubRepository, revision: Optional[str]
):
    return f"Revision {revision} not found for repository {repository.owner}/{repository.name}"


def repository_not_found_error_message(repository: GithubRepository):
    return f"Could not find release for {repository.owner}/{repository.name}"


@dataclass(frozen=True)
class _Prefetcher:
    url_hasher: UrlHasher
    revision_index_factory: RevisionIndexFactory

    @do
    def prefetch_github(
        self,
        repository: GithubRepository,
        rev: Optional[str],
        prefetch_options: PrefetchOptions,
    ):
        revision: Optional[str]
        if rev is not None and self._is_proper_revision_hash(rev):
            revision = rev
        else:
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
        return (yield self._prefetch_github(repository, revision, prefetch_options))

    @do
    def prefetch_latest_release(
        self,
        repository: GithubRepository,
        prefetch_options: PrefetchOptions,
    ):
        revision = yield Effect(GetRevisionForLatestRelease(repository=repository))
        if not revision:
            yield Effect(
                AbortWithErrorMessage(repository_not_found_error_message(repository))
            )
            raise AbortWithError()
        return (yield self._prefetch_github(repository, revision, prefetch_options))

    @do
    def _prefetch_github(
        self,
        repository: GithubRepository,
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
        return PrefetchedRepository(
            repository=repository,
            sha256=cast(str, calculated_hash),
            rev=revision,
            fetch_submodules=prefetch_options.fetch_submodules,
        )

    def _is_proper_revision_hash(self, revision: str) -> bool:
        return is_sha1_hash(revision)

    def _detect_revision(
        self, repository: GithubRepository, revision: Optional[str]
    ) -> Optional[str]:
        actual_rev: Optional[str]
        revision_index = self.revision_index_factory.get_revision_index(repository)
        if revision_index is None:
            return None
        if revision is None:
            actual_rev = revision_index.get_revision_by_name("HEAD")
        else:
            actual_rev = revision_index.get_revision_by_name(cast(str, revision))
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


@dataclass(frozen=True)
class PrefetchedRepository:
    repository: GithubRepository
    rev: str
    sha256: str
    fetch_submodules: bool

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


class RevisionIndexFactory(Protocol):
    def get_revision_index(
        self, repository: GithubRepository
    ) -> Optional[RevisionIndex]:
        ...


def prefetch_github(
    url_hasher: UrlHasher,
    revision_index_factory: RevisionIndexFactory,
    repository: GithubRepository,
    rev: Optional[str] = None,
    fetch_submodules: bool = True,
):
    prefetcher = _Prefetcher(url_hasher, revision_index_factory)
    return prefetcher.prefetch_github(
        repository=repository,
        rev=rev,
        prefetch_options=PrefetchOptions(fetch_submodules=fetch_submodules),
    )


def prefetch_latest_release(
    url_hasher: UrlHasher,
    revision_index_factory: RevisionIndexFactory,
    repository: GithubRepository,
    fetch_submodules: bool,
):
    prefetcher = _Prefetcher(url_hasher, revision_index_factory)
    return prefetcher.prefetch_latest_release(
        repository=repository,
        prefetch_options=PrefetchOptions(fetch_submodules=fetch_submodules),
    )
