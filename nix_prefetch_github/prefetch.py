from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .hash import is_sha1_hash
from .interfaces import (
    GithubRepository,
    PrefetchedRepository,
    PrefetchFailure,
    PrefetchOptions,
    PrefetchResult,
    RevisionIndexFactory,
    UrlHasher,
)


@dataclass(frozen=True)
class PrefetcherImpl:
    url_hasher: UrlHasher
    revision_index_factory: RevisionIndexFactory

    def prefetch_github(
        self,
        repository: GithubRepository,
        rev: Optional[str],
        prefetch_options: PrefetchOptions,
    ) -> PrefetchResult:
        revision: Optional[str]
        if rev is not None and self._is_proper_revision_hash(rev):
            revision = rev
        else:
            revision = self._detect_revision(repository, rev)
        if revision is None:
            return PrefetchFailure(
                reason=PrefetchFailure.Reason.unable_to_locate_revision
            )
        return self._prefetch_github(repository, revision, prefetch_options)

    def _prefetch_github(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> PrefetchResult:
        calculated_hash = self._calculate_sha256_sum(
            repository, revision, prefetch_options
        )
        if calculated_hash is None:
            return PrefetchFailure(
                reason=PrefetchFailure.Reason.unable_to_calculate_sha256
            )
        return PrefetchedRepository(
            repository=repository,
            sha256=calculated_hash,
            rev=revision,
            options=prefetch_options,
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
            actual_rev = revision_index.get_revision_by_name(revision)
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
