import json

from attr import attrib, attrs
from effect import Effect
from effect.do import do

from nix_prefetch_github.templates import output_template

from .effects import AbortWithErrorMessage, CalculateSha256Sum, TryPrefetch
from .error import AbortWithError
from .hash import is_sha1_hash
from .revision import RevisionIndex


def revision_not_found_errormessage(repository, revision):
    return f"Revision {revision} not found for repository {repository.owner}/{repository.name}"


def repository_not_found_error_message(repository):
    return f"Could not find release for {repository.owner}/{repository.name}"


class _Prefetcher:
    def __init__(self, repository):
        self._repository = repository
        self._revision_index = RevisionIndex(repository)
        self._prefetched_repository = None
        self._calculated_hash = None
        self._prefetch = None
        self._revision = None
        self._fetch_submodules = None

    @do
    def prefetch_github(self, prefetch, rev, fetch_submodules):
        self._prefetch = prefetch
        self._revision = rev
        self._fetch_submodules = fetch_submodules
        yield self._detect_revision()
        yield self._calculate_sha256_sum()
        yield self._prefetch_repository()
        return self._prefetched_repository

    @do
    def prefetch_latest_release(self, prefetch, fetch_submodules):
        self._prefetch = prefetch
        self._fetch_submodules = fetch_submodules
        self._revision = yield self._revision_index.get_revision_for_latest_release()
        if not self._revision:
            yield Effect(
                AbortWithErrorMessage(
                    repository_not_found_error_message(self._repository)
                )
            )
            raise AbortWithError()
        yield self._calculate_sha256_sum()
        yield self._prefetch_repository()
        return self._prefetched_repository

    @do
    def _detect_revision(self):
        if isinstance(self._revision, str) and is_sha1_hash(self._revision):
            actual_rev = self._revision
        else:
            actual_rev = yield self._revision_index.get_revision_from_name(
                self._revision
            )
        if actual_rev is None:
            yield Effect(
                AbortWithErrorMessage(
                    message=revision_not_found_errormessage(
                        repository=self._repository, revision=self._revision
                    )
                )
            )
            raise AbortWithError()
        self._revision = actual_rev

    @do
    def _calculate_sha256_sum(self):
        self._calculated_hash = yield Effect(
            CalculateSha256Sum(
                repository=self._repository,
                revision=self._revision,
                fetch_submodules=self._fetch_submodules,
            )
        )
        if not self._calculated_hash:
            yield Effect(
                AbortWithErrorMessage(
                    message=(
                        "Internal Error: Calculate hash value for sources "
                        f"in github repo {self._repository.owner}/{self._repository.name}."
                    )
                )
            )

    @do
    def _prefetch_repository(self):
        if self._prefetch:
            yield Effect(
                TryPrefetch(
                    repository=self._repository,
                    sha256=self._calculated_hash,
                    rev=self._revision,
                    fetch_submodules=self._fetch_submodules,
                )
            )
        self._prefetched_repository = PrefetchedRepository(
            repository=self._repository,
            sha256=self._calculated_hash,
            rev=self._revision,
            fetch_submodules=self._prefetch,
        )


@attrs
class PrefetchedRepository:
    repository = attrib()
    rev = attrib()
    sha256 = attrib()
    fetch_submodules = attrib()

    def to_nix_expression(self):
        return output_template.render(
            owner=self.repository.owner,
            repo=self.repository.name,
            rev=self.rev,
            sha256=self.sha256,
            fetch_submodules="true" if self.fetch_submodules else "false",
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


def prefetch_github(repository, prefetch=True, rev=None, fetch_submodules=True):
    prefetcher = _Prefetcher(repository)
    return prefetcher.prefetch_github(
        prefetch=prefetch, rev=rev, fetch_submodules=fetch_submodules
    )


def prefetch_latest_release(repository, prefetch, fetch_submodules):
    prefetcher = _Prefetcher(repository=repository)
    return prefetcher.prefetch_latest_release(
        prefetch=prefetch, fetch_submodules=fetch_submodules
    )
