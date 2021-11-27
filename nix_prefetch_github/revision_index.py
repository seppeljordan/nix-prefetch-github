from dataclasses import dataclass
from logging import Logger
from typing import Optional, Protocol

from .core import GithubRepository, ListRemote, RevisionIndex


class RemoteListFactory(Protocol):
    def get_remote_list(self, repository: GithubRepository) -> Optional[ListRemote]:
        ...


@dataclass
class RevisionIndexFactoryImpl:
    remote_list_factory: RemoteListFactory
    logger: Logger

    def get_revision_index(
        self, repository: GithubRepository
    ) -> Optional[RevisionIndex]:
        remote_list = self.remote_list_factory.get_remote_list(repository)
        if remote_list is None:
            self.logger.error(f"Could not download git references for {repository}")
            return None
        return RevisionIndex(remote_list)
