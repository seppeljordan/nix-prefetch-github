from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from nix_prefetch_github.hash import is_sha1_hash
from nix_prefetch_github.interfaces import (
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
        prefetched_repo = self.url_hasher.calculate_hash_sum(
            repository=repository,
            revision=revision,
            prefetch_options=prefetch_options,
        )
        if prefetched_repo is None:
            return PrefetchFailure(
                reason=PrefetchFailure.Reason.unable_to_calculate_hash_sum
            )
        return PrefetchedRepository(
            repository=repository,
            hash_sum=prefetched_repo.hash_sum,
            rev=revision,
            options=prefetch_options,
            store_path=prefetched_repo.store_path,
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
