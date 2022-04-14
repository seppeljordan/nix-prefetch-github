import enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Tuple, Union

from .list_remote import ListRemote
from .revision_index import RevisionIndex


@dataclass(frozen=True)
class GithubRepository:
    owner: str
    name: str

    def url(self) -> str:
        return f"https://github.com/{self.owner}/{self.name}.git"


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
    options: PrefetchOptions


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


class CommandRunner(Protocol):
    def run_command(
        self,
        command: List[str],
        cwd: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        merge_stderr: bool = False,
    ) -> Tuple[int, str]:
        ...


class CommandAvailabilityChecker(Protocol):
    def is_command_available(self, command: str) -> bool:
        ...


class RepositoryRenderer(Protocol):
    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        ...


class Presenter(Protocol):
    def present(self, prefetch_result: PrefetchResult) -> int:
        ...


@enum.unique
class RenderingFormat(enum.Enum):
    nix = enum.auto()
    json = enum.auto()
