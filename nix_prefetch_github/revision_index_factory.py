from dataclasses import dataclass
from typing import Optional

from .functor import map_or_none
from .interfaces import ListRemoteFactory
from .repository import GithubRepository
from .revision_index import RevisionIndex


@dataclass(frozen=True)
class RevisionIndexFactoryImpl:
    list_remote_factory: ListRemoteFactory

    def get_revision_index(
        self, repository: GithubRepository
    ) -> Optional[RevisionIndex]:
        return map_or_none(
            RevisionIndex, self.list_remote_factory.get_list_remote(repository)
        )
