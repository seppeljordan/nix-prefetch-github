from dataclasses import dataclass
from typing import Optional, Protocol

from .list_remote import ListRemote
from .repository import GithubRepository


class RemoteListFactory(Protocol):
    def get_remote_list(self, repository: GithubRepository) -> Optional[ListRemote]:
        ...


@dataclass(frozen=True)
class RevisionIndex:
    remote_list_factory: RemoteListFactory

    def get_revision_by_name(
        self, repository: GithubRepository, name: str
    ) -> Optional[str]:
        remote_list = self.remote_list_factory.get_remote_list(repository)
        if remote_list is None:
            return None
        if (symref := remote_list.symref(name)) is not None:
            name = symref
        return (
            remote_list.full_ref_name(name)
            or remote_list.branch(name)
            or remote_list.tag(f"{name}^{{}}")
            or remote_list.tag(name)
        )
