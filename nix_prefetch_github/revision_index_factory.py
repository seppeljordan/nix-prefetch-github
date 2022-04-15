from dataclasses import dataclass
from typing import Optional, Protocol

from .functor import map_or_none
from .interfaces import GithubRepository
from .list_remote import ListRemote
from .revision_index import RevisionIndexImpl


class ListRemoteFactory(Protocol):
    def get_list_remote(self, repository: GithubRepository) -> Optional[ListRemote]:
        pass


@dataclass(frozen=True)
class RevisionIndexFactoryImpl:
    list_remote_factory: ListRemoteFactory

    def get_revision_index(
        self, repository: GithubRepository
    ) -> Optional[RevisionIndexImpl]:
        return map_or_none(
            RevisionIndexImpl, self.list_remote_factory.get_list_remote(repository)
        )
