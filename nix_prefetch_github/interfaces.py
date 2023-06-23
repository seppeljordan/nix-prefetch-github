from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol, Tuple, Union


class Alerter(Protocol):
    def alert_user_about_unsafe_prefetch_options(
        self, prefetch_options: PrefetchOptions
    ) -> None:
        ...


class RevisionIndex(Protocol):
    def get_revision_by_name(self, name: str) -> Optional[str]:
        ...


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

    def is_safe(self) -> bool:
        return not self.deep_clone and not self.leave_dot_git


class HashConverter(Protocol):
    def convert_sha256_to_sri(self, original: str) -> Optional[str]:
        ...


class UrlHasher(Protocol):
    def calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        ...


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
    def present(self, prefetch_result: PrefetchResult) -> None:
        ...


@enum.unique
class RenderingFormat(enum.Enum):
    nix = enum.auto()
    json = enum.auto()


class RenderingFormatSelector(Protocol):
    def set_rendering_format(self, rendering_format: RenderingFormat) -> None:
        ...


@dataclass
class ViewModel:
    exit_code: int
    stderr_lines: List[str]
    stdout_lines: List[str]


class CommandLineView(Protocol):
    def render_view_model(self, model: ViewModel) -> None:
        ...
