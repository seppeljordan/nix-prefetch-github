from effect import Effect
from effect.do import do

from .effects import GetListRemote, GetRevisionForLatestRelease


class RevisionIndex:
    def __init__(self, repository):
        self._repository = repository

    @do
    def get_revision_from_name(self, revision_name):
        list_remote = yield Effect(GetListRemote(repository=self._repository))
        if revision_name is None:
            return list_remote.branch(list_remote.symref("HEAD"))
        return (
            list_remote.full_ref_name(revision_name)
            or list_remote.branch(revision_name)
            or list_remote.tag(f"{revision_name}^{{}}")
            or list_remote.tag(revision_name)
        )

    def get_revision_for_latest_release(self):
        return Effect(GetRevisionForLatestRelease(repository=self._repository))
