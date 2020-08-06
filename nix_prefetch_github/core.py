import re

from attr import attrib, attrs
from effect import Constant, Effect
from effect.do import do

from .error import AbortWithErrorMessage, revision_not_found_errormessage


def is_sha1_hash(text):
    return re.match(r"^[0-9a-f]{40}$", text)


@attrs
class GetListRemote:
    owner = attrib()
    repo = attrib()


@attrs
class TryPrefetch(object):
    owner = attrib()
    repo = attrib()
    sha256 = attrib()
    rev = attrib()
    fetch_submodules = attrib(default=False)


@attrs
class CalculateSha256Sum:
    owner = attrib()
    repo = attrib()
    revision = attrib()
    fetch_submodules = attrib(default=False)


@do
def prefetch_github(owner, repo, prefetch=True, rev=None, fetch_submodules=False):
    if isinstance(rev, str) and is_sha1_hash(rev):
        actual_rev = rev
    else:
        list_remote = yield Effect(GetListRemote(owner=owner, repo=repo))
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
    return Effect(Constant({"rev": actual_rev, "sha256": calculated_hash}))
