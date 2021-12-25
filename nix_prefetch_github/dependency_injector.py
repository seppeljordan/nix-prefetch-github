from functools import lru_cache
from logging import Logger

from .command import CommandRunner
from .github import GithubAPIImpl
from .interfaces import GithubAPI, RepositoryDetector, RevisionIndexFactory, UrlHasher
from .list_remote_factory import ListRemoteFactoryImpl
from .logging import LoggingConfiguration, get_logger
from .prefetch import PrefetcherImpl
from .repository_detector import RepositoryDetectorImpl
from .revision_index_factory import RevisionIndexFactoryImpl
from .url_hasher import UrlHasherImpl


class DependencyInjector:
    def __init__(self, logging_configuration: LoggingConfiguration) -> None:
        self._logging_configuration = logging_configuration

    def get_revision_index_factory(self) -> RevisionIndexFactory:
        return RevisionIndexFactoryImpl(self.get_remote_list_factory())

    def get_remote_list_factory(self) -> ListRemoteFactoryImpl:
        return ListRemoteFactoryImpl(command_runner=self.get_command_runner())

    def get_url_hasher(self) -> UrlHasher:
        return UrlHasherImpl(command_runner=self.get_command_runner())

    def get_prefetcher(self) -> PrefetcherImpl:
        return PrefetcherImpl(self.get_url_hasher(), self.get_revision_index_factory())

    def get_github_api(self) -> GithubAPI:
        return GithubAPIImpl()

    def get_repository_detector(self) -> RepositoryDetector:
        return RepositoryDetectorImpl(command_runner=self.get_command_runner())

    def get_command_runner(self) -> CommandRunner:
        return CommandRunner(logger=self.get_logger())

    @lru_cache()
    def get_logger(self) -> Logger:
        return get_logger(self.get_logging_configuration())

    def get_logging_configuration(self) -> LoggingConfiguration:
        return self._logging_configuration
