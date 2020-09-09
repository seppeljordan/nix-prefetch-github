import json

from attr import attrib, attrs
from effect import Constant, Effect
from effect.do import do

from nix_prefetch_github.templates import output_template

from .effects import (
    AbortWithErrorMessage,
    CalculateSha256Sum,
    GetListRemote,
    TryPrefetch,
)
from .error import AbortWithError
from .hash import is_sha1_hash
from .wrapper import wraps_with_namechange


def revision_not_found_errormessage(repository, revision):
    return f"Revision {revision} not found for repository {repository.owner}/{repository.name}"


class _Prefetcher:
    def __init__(self, repository, prefetch=True, rev=None, fetch_submodules=True):
        self._repository = repository
        self._prefetch = prefetch
        self._revision = rev
        self._fetch_submodules = fetch_submodules

    @do
    def prefetch_github(self):
        yield self._detect_revision()
        calculated_hash = yield self._calculate_sha256_sum()
        yield self._prefetch_repository(calculated_hash)
        return Effect(
            Constant(
                PrefetchedRepository(
                    repository=self._repository,
                    sha256=calculated_hash,
                    rev=self._revision,
                    fetch_submodules=self._prefetch,
                )
            )
        )

    @do
    def _detect_revision(self):
        if isinstance(self._revision, str) and is_sha1_hash(self._revision):
            actual_rev = self._revision
        else:
            list_remote = yield Effect(GetListRemote(repository=self._repository))
            if not list_remote:
                yield Effect(
                    AbortWithErrorMessage(
                        f"Could not find a public repository named '{self._repository.name}' for user '{self._repository.owner}' at github.com"
                    )
                )
            if self._revision is None:
                actual_rev = list_remote.branch(list_remote.symref("HEAD"))
            else:
                actual_rev = (
                    list_remote.full_ref_name(self._revision)
                    or list_remote.branch(self._revision)
                    or list_remote.tag(f"{self._revision}^{{}}")
                    or list_remote.tag(self._revision)
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
        calculated_hash = yield Effect(
            CalculateSha256Sum(
                repository=self._repository,
                revision=self._revision,
                fetch_submodules=self._fetch_submodules,
            )
        )
        if not calculated_hash:
            yield Effect(
                AbortWithErrorMessage(
                    message=(
                        "Internal Error: Calculate hash value for sources "
                        f"in github repo {self._repository.owner}/{self._repository.name}."
                    )
                )
            )
        return calculated_hash

    @do
    def _prefetch_repository(self, calculated_hash):
        if self._prefetch:
            yield Effect(
                TryPrefetch(
                    repository=self._repository,
                    sha256=calculated_hash,
                    rev=self._revision,
                    fetch_submodules=self._fetch_submodules,
                )
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


@wraps_with_namechange(_Prefetcher)
def prefetch_github(*args, **kwargs):
    prefetcher = _Prefetcher(*args, **kwargs)
    return prefetcher.prefetch_github()
