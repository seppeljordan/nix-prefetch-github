from dataclasses import dataclass
from typing import Optional, Protocol

from nix_prefetch_github.functor import map_or_none
from nix_prefetch_github.interfaces import GithubRepository
from nix_prefetch_github.list_remote import ListRemote
from nix_prefetch_github.revision_index import RevisionIndexImpl


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
