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
from .hash import is_sha1_hash


def revision_not_found_errormessage(repository, revision):
    return f"Revision {revision} not found for repository {repository.owner}/{repository.name}"


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


@do
def prefetch_github(repository, prefetch=True, rev=None, fetch_submodules=True):
    if isinstance(rev, str) and is_sha1_hash(rev):
        actual_rev = rev
    else:
        list_remote = yield Effect(GetListRemote(repository=repository))
        if not list_remote:
            yield Effect(
                AbortWithErrorMessage(
                    f"Could not find a public repository named '{repository.name}' for user '{repository.owner}' at github.com"
                )
            )
        if rev is None:
            actual_rev = list_remote.branch(list_remote.symref("HEAD"))
        else:
            actual_rev = (
                list_remote.full_ref_name(rev)
                or list_remote.branch(rev)
                or list_remote.tag(f"{rev}^{{}}")
                or list_remote.tag(rev)
            )
            if actual_rev is None:
                yield Effect(
                    AbortWithErrorMessage(
                        message=revision_not_found_errormessage(
                            repository=repository, revision=rev
                        )
                    )
                )
                return

    calculated_hash = yield Effect(
        CalculateSha256Sum(
            repository=repository,
            revision=actual_rev,
            fetch_submodules=fetch_submodules,
        )
    )
    if not calculated_hash:
        yield Effect(
            AbortWithErrorMessage(
                message=(
                    "Internal Error: Calculate hash value for sources "
                    f"in github repo {repository.owner}/{repository.name}."
                )
            )
        )
    if prefetch:
        yield Effect(
            TryPrefetch(
                repository=repository,
                sha256=calculated_hash,
                rev=actual_rev,
                fetch_submodules=fetch_submodules,
            )
        )
    return Effect(
        Constant(
            PrefetchedRepository(
                repository=repository,
                sha256=calculated_hash,
                rev=actual_rev,
                fetch_submodules=prefetch,
            )
        )
    )
