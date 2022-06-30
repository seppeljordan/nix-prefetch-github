from functools import lru_cache
from logging import Logger

from nix_prefetch_github.alerter import CliAlerterImpl
from nix_prefetch_github.command.command_availability_checker import (
    CommandAvailabilityCheckerImpl,
)
from nix_prefetch_github.command.command_runner import CommandRunnerImpl
from nix_prefetch_github.controller.nix_prefetch_github_controller import (
    NixPrefetchGithubController,
)
from nix_prefetch_github.controller.prefetch_directory_controller import (
    PrefetchDirectoryController,
)
from nix_prefetch_github.controller.prefetch_latest_release_controller import (
    PrefetchLatestReleaseController,
)
from nix_prefetch_github.github import GithubAPIImpl
from nix_prefetch_github.interfaces import (
    GithubAPI,
    RepositoryDetector,
    RevisionIndexFactory,
)
from nix_prefetch_github.list_remote_factory import ListRemoteFactoryImpl
from nix_prefetch_github.logging import LoggerFactoryImpl
from nix_prefetch_github.prefetch import PrefetcherImpl
from nix_prefetch_github.presenter import (
    JsonRepositoryRenderer,
    NixRepositoryRenderer,
    PresenterImpl,
)
from nix_prefetch_github.process_environment import ProcessEnvironmentImpl
from nix_prefetch_github.repository_detector import RepositoryDetectorImpl
from nix_prefetch_github.revision_index_factory import RevisionIndexFactoryImpl
from nix_prefetch_github.url_hasher.nix_build import NixBuildUrlHasherImpl
from nix_prefetch_github.url_hasher.nix_prefetch import NixPrefetchUrlHasherImpl
from nix_prefetch_github.url_hasher.url_hasher_selector import (
    CommandAvailabilityChecker,
    UrlHasherSelector,
)
from nix_prefetch_github.use_cases.prefetch_directory import (
    PrefetchDirectoryUseCaseImpl,
)
from nix_prefetch_github.use_cases.prefetch_github_repository import (
    PrefetchGithubRepositoryUseCaseImpl,
)
from nix_prefetch_github.use_cases.prefetch_latest_release import (
    PrefetchLatestReleaseUseCaseImpl,
)
from nix_prefetch_github.views import CommandLineViewImpl


class DependencyInjector:
    def get_alerter(self) -> CliAlerterImpl:
        return CliAlerterImpl(
            logger=self.get_logger(),
        )

    def get_revision_index_factory(self) -> RevisionIndexFactory:
        return RevisionIndexFactoryImpl(self.get_remote_list_factory())

    def get_process_environment(self) -> ProcessEnvironmentImpl:
        return ProcessEnvironmentImpl()

    def get_remote_list_factory(self) -> ListRemoteFactoryImpl:
        return ListRemoteFactoryImpl(command_runner=self.get_command_runner())

    def get_view(self) -> CommandLineViewImpl:
        return CommandLineViewImpl()

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

    def get_prefetcher(self) -> PrefetcherImpl:
        return PrefetcherImpl(
            self.get_url_hasher_selector(), self.get_revision_index_factory()
        )

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
    def get_logger_factory(self) -> LoggerFactoryImpl:
        return LoggerFactoryImpl()

    def get_logger(self) -> Logger:
        factory = self.get_logger_factory()
        return factory.get_logger()

    def get_nix_presenter(self) -> PresenterImpl:
        return PresenterImpl(
            view=self.get_view(),
            repository_renderer=self.get_nix_repository_renderer(),
        )

    def get_json_presenter(self) -> PresenterImpl:
        return PresenterImpl(
            view=self.get_view(),
            repository_renderer=self.get_json_repository_renderer(),
        )

    def get_prefetch_latest_release_use_case(self) -> PrefetchLatestReleaseUseCaseImpl:
        return PrefetchLatestReleaseUseCaseImpl(
            nix_presenter=self.get_nix_presenter(),
            json_presenter=self.get_json_presenter(),
            prefetcher=self.get_prefetcher(),
            github_api=self.get_github_api(),
        )

    def get_prefetch_github_repository_use_case(
        self,
    ) -> PrefetchGithubRepositoryUseCaseImpl:
        return PrefetchGithubRepositoryUseCaseImpl(
            nix_presenter=self.get_nix_presenter(),
            json_presenter=self.get_json_presenter(),
            prefetcher=self.get_prefetcher(),
            alerter=self.get_alerter(),
        )

    def get_prefetch_directory_use_case(self) -> PrefetchDirectoryUseCaseImpl:
        return PrefetchDirectoryUseCaseImpl(
            nix_presenter=self.get_nix_presenter(),
            json_presenter=self.get_json_presenter(),
            prefetcher=self.get_prefetcher(),
            repository_detector=self.get_repository_detector(),
            logger=self.get_logger(),
        )

    def get_prefetch_github_repository_controller(self) -> NixPrefetchGithubController:
        return NixPrefetchGithubController(
            use_case=self.get_prefetch_github_repository_use_case(),
            logger_manager=self.get_logger_factory(),
        )

    def get_prefetch_latest_release_controller(self) -> PrefetchLatestReleaseController:
        return PrefetchLatestReleaseController(
            use_case=self.get_prefetch_latest_release_use_case(),
            logger_manager=self.get_logger_factory(),
        )

    def get_prefetch_directory_controller(self) -> PrefetchDirectoryController:
        return PrefetchDirectoryController(
            logger_manager=self.get_logger_factory(),
            use_case=self.get_prefetch_directory_use_case(),
            environment=self.get_process_environment(),
        )
