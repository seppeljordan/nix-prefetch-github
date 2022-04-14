import sys
from functools import lru_cache
from logging import Logger

from .command.command_availability_checker import CommandAvailabilityCheckerImpl
from .command.command_runner import CommandRunnerImpl
from .github import GithubAPIImpl
from .interfaces import GithubAPI, RepositoryDetector, RevisionIndexFactory, UrlHasher
from .list_remote_factory import ListRemoteFactoryImpl
from .logging import LoggingConfiguration, get_logger
from .prefetch import PrefetcherImpl
from .presenter import (
    Presenter,
    RenderingFormat,
    RepositoryRenderer,
    get_renderer_from_rendering_format,
)
from .repository_detector import RepositoryDetectorImpl
from .revision_index_factory import RevisionIndexFactoryImpl
from .url_hasher.nix_build import NixBuildUrlHasherImpl
from .url_hasher.nix_prefetch import NixPrefetchUrlHasherImpl
from .url_hasher.url_hasher_selector import (
    CommandAvailabilityChecker,
    UrlHasherSelector,
)


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

    def get_presenter(self) -> Presenter:
        return Presenter(
            result_output=sys.stdout,
            error_output=sys.stderr,
            repository_renderer=self.get_repository_renderer(),
        )

    def get_repository_renderer(self) -> RepositoryRenderer:
        return get_renderer_from_rendering_format(self._rendering_format)

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
