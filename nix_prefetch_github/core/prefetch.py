import json
import re

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


def is_sha1_hash(text):
    return re.match(r"^[0-9a-f]{40}$", text)


def revision_not_found_errormessage(owner, repo, revision):
    return "Revision {revision} not found for repository {owner}/{repo}".format(
        revision=revision, owner=owner, repo=repo
    )


def github_repository_url(owner, repo):
    return f"https://github.com/{owner}/{repo}.git"


@attrs
class PrefetchedRepository:
    owner = attrib()
    repo = attrib()
    rev = attrib()
    sha256 = attrib()
    fetch_submodules = attrib()

    def to_nix_expression(self):
        return output_template.render(
            owner=self.owner,
            repo=self.repo,
            rev=self.rev,
            sha256=self.sha256,
            fetch_submodules="true" if self.fetch_submodules else "false",
        )

    def to_json_string(self):
        return json.dumps(
            {
                "owner": self.owner,
                "repo": self.repo,
                "rev": self.rev,
                "sha256": self.sha256,
                "fetchSubmodules": self.fetch_submodules,
            },
            indent=4,
        )


@attrs
class GithubRepository:
    name = attrib()
    owner = attrib()


@do
def prefetch_github(owner, repo, prefetch=True, rev=None, fetch_submodules=False):
    if isinstance(rev, str) and is_sha1_hash(rev):
        actual_rev = rev
    else:
        list_remote = yield Effect(GetListRemote(owner=owner, repo=repo))
        if not list_remote:
            yield Effect(
                AbortWithErrorMessage(
                    f"Could not find a public repository named '{repo}' for user '{owner}' at github.com"
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
                            owner=owner, repo=repo, revision=rev
                        )
                    )
                )
                return

    calculated_hash = yield Effect(
        CalculateSha256Sum(
            owner=owner,
            repo=repo,
            revision=actual_rev,
            fetch_submodules=fetch_submodules,
        )
    )
    if not calculated_hash:
        yield Effect(
            AbortWithErrorMessage(
                message=(
                    "Internal Error: Calculate hash value for sources "
                    "in github repo {owner}/{repo}."
                ).format(owner=owner, repo=repo)
            )
        )
    if prefetch:
        yield Effect(
            TryPrefetch(owner=owner, repo=repo, sha256=calculated_hash, rev=actual_rev)
        )
    return Effect(
        Constant(
            PrefetchedRepository(
                owner=owner,
                repo=repo,
                sha256=calculated_hash,
                rev=actual_rev,
                fetch_submodules=prefetch,
            )
        )
    )
