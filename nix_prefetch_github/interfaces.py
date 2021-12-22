import enum
from dataclasses import dataclass
from typing import Optional, Protocol, Union

from .list_remote import ListRemote
from .repository import GithubRepository
from .revision_index import RevisionIndex

trash_sha256 = "1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv"


@dataclass
class PrefetchOptions:
    fetch_submodules: bool = False
    deep_clone: bool = False
    leave_dot_git: bool = False


class UrlHasher(Protocol):
    def calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        pass


class GithubAPI(Protocol):
    def get_tag_of_latest_release(self, repository: GithubRepository) -> Optional[str]:
        ...


class RevisionIndexFactory(Protocol):
    def get_revision_index(
        self, repository: GithubRepository
    ) -> Optional[RevisionIndex]:
        ...


class RepositoryDetector(Protocol):
    def detect_github_repository(
        self, directory: str, remote_name: Optional[str]
    ) -> Optional[GithubRepository]:
        ...

    def is_repository_dirty(self, directory: str) -> bool:
        ...

    def get_current_revision(self, directory: str) -> Optional[str]:
        ...


class ListRemoteFactory(Protocol):
    def get_list_remote(self, repository: GithubRepository) -> Optional[ListRemote]:
        pass


@dataclass(frozen=True)
class PrefetchedRepository:
    repository: GithubRepository
    rev: str
    sha256: str
    fetch_submodules: bool


@dataclass
class PrefetchFailure:
    class Reason(enum.Enum):
        unable_to_locate_revision = enum.auto()
        unable_to_calculate_sha256 = enum.auto()

        def __str__(self) -> str:
            if self == self.unable_to_calculate_sha256:
                return "Unable to calculate sha256 sum"
            else:
                return "Unable to locate revision"

    reason: Reason


PrefetchResult = Union[PrefetchedRepository, PrefetchFailure]


class Prefetcher(Protocol):
    def prefetch_github(
        self,
        repository: GithubRepository,
        rev: Optional[str],
        prefetch_options: PrefetchOptions,
    ) -> PrefetchResult:
        ...
