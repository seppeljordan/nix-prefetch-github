import sys
from functools import lru_cache
from logging import Logger

from .command.command_availability_checker import CommandAvailabilityCheckerImpl
from .command.command_runner import CommandRunnerImpl
from .github import GithubAPIImpl
from .interfaces import (
    GithubAPI,
    RenderingFormat,
    RepositoryDetector,
    RevisionIndexFactory,
    UrlHasher,
)
from .list_remote_factory import ListRemoteFactoryImpl
from .logging import LoggingConfiguration, get_logger
from .prefetch import PrefetcherImpl
from .presenter import JsonRepositoryRenderer, NixRepositoryRenderer, PresenterImpl
from .repository_detector import RepositoryDetectorImpl
from .revision_index_factory import RevisionIndexFactoryImpl
from .url_hasher.nix_build import NixBuildUrlHasherImpl
from .url_hasher.nix_prefetch import NixPrefetchUrlHasherImpl
from .url_hasher.url_hasher_selector import (
    CommandAvailabilityChecker,
    UrlHasherSelector,
)
from .use_cases.prefetch_directory import PrefetchDirectoryUseCase
from .use_cases.prefetch_github_repository import PrefetchGithubRepositoryUseCase
from .use_cases.prefetch_latest_release import PrefetchLatestReleaseUseCase


class DependencyInjector:
    def __init__(
        self,
        logging_configuration: LoggingConfiguration,
        rendering_format: RenderingFormat,
    ) -> None:
        self._logging_configuration = logging_configuration
        self._rendering_format = rendering_format

    def get_revision_index_factory(self) -> RevisionIndexFactory:
        return RevisionIndexFactoryImpl(self.get_remote_list_factory())

    def get_remote_list_factory(self) -> ListRemoteFactoryImpl:
        return ListRemoteFactoryImpl(command_runner=self.get_command_runner())

    def get_url_hasher_selector(self) -> UrlHasherSelector:
        return UrlHasherSelector(
            availability_checker=self.get_command_availability_checker(),
            nix_build_implementation=self.get_nix_build_url_hasher_impl(),
            nix_prefetch_implementation=self.get_nix_prefetch_url_hasher_impl(),
        )

    def get_command_availability_checker(self) -> CommandAvailabilityChecker:
        return CommandAvailabilityCheckerImpl(command_runner=self.get_command_runner())

    def get_nix_build_url_hasher_impl(self) -> NixBuildUrlHasherImpl:
        return NixBuildUrlHasherImpl(
            command_runner=self.get_command_runner(), logger=self.get_logger()
        )

    def get_nix_prefetch_url_hasher_impl(self) -> NixPrefetchUrlHasherImpl:
        return NixPrefetchUrlHasherImpl(
            command_runner=self.get_command_runner(), logger=self.get_logger()
        )

    def get_url_hasher(self) -> UrlHasher:
        selector = self.get_url_hasher_selector()
        return selector.get_url_hasher()

    def get_prefetcher(self) -> PrefetcherImpl:
        return PrefetcherImpl(self.get_url_hasher(), self.get_revision_index_factory())

    def get_nix_repository_renderer(self) -> NixRepositoryRenderer:
        return NixRepositoryRenderer()

    def get_json_repository_renderer(self) -> JsonRepositoryRenderer:
        return JsonRepositoryRenderer()

    def get_github_api(self) -> GithubAPI:
        return GithubAPIImpl()

    def get_repository_detector(self) -> RepositoryDetector:
        return RepositoryDetectorImpl(command_runner=self.get_command_runner())

    def get_command_runner(self) -> CommandRunnerImpl:
        return CommandRunnerImpl(logger=self.get_logger())

    @lru_cache()
    def get_logger(self) -> Logger:
        return get_logger(self.get_logging_configuration())

    def get_logging_configuration(self) -> LoggingConfiguration:
        return self._logging_configuration

    def get_nix_presenter(self) -> PresenterImpl:
        return PresenterImpl(
            result_output=sys.stdout,
            error_output=sys.stderr,
            repository_renderer=self.get_nix_repository_renderer(),
        )

    def get_json_presenter(self) -> PresenterImpl:
        return PresenterImpl(
            result_output=sys.stdout,
            error_output=sys.stderr,
            repository_renderer=self.get_nix_repository_renderer(),
        )

    def get_prefetch_latest_release_use_case(self) -> PrefetchLatestReleaseUseCase:
        return PrefetchLatestReleaseUseCase(
            nix_presenter=self.get_nix_presenter(),
            json_presenter=self.get_json_presenter(),
            prefetcher=self.get_prefetcher(),
            github_api=self.get_github_api(),
        )

    def get_prefetch_github_repository_use_case(
        self,
    ) -> PrefetchGithubRepositoryUseCase:
        return PrefetchGithubRepositoryUseCase(
            nix_presenter=self.get_nix_presenter(),
            json_presenter=self.get_json_presenter(),
            prefetcher=self.get_prefetcher(),
        )

    def get_prefetch_directory_use_case(self) -> PrefetchDirectoryUseCase:
        return PrefetchDirectoryUseCase(
            nix_presenter=self.get_nix_presenter(),
            json_presenter=self.get_json_presenter(),
            prefetcher=self.get_prefetcher(),
            repository_detector=self.get_repository_detector(),
            logger=self.get_logger(),
        )
