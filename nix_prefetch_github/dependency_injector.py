from logging import Logger, getLogger

from .github import GithubAPIImpl
from .interfaces import GithubAPI, RepositoryDetector, RevisionIndexFactory, UrlHasher
from .list_remote_factory import ListRemoteFactoryImpl
from .prefetch import PrefetcherImpl
from .repository_detector import RepositoryDetectorImpl
from .revision_index_factory import RevisionIndexFactoryImpl
from .url_hasher import UrlHasherImpl


class DependencyInjector:
    def get_revision_index_factory(self) -> RevisionIndexFactory:
        return RevisionIndexFactoryImpl(self.get_remote_list_factory())

    def get_remote_list_factory(self) -> ListRemoteFactoryImpl:
        return ListRemoteFactoryImpl()

    def get_logger(self) -> Logger:
        return getLogger()

    def get_url_hasher(self) -> UrlHasher:
        return UrlHasherImpl()

    def get_prefetcher(self) -> PrefetcherImpl:
        return PrefetcherImpl(self.get_url_hasher(), self.get_revision_index_factory())

    def get_github_api(self) -> GithubAPI:
        return GithubAPIImpl()

    def get_repository_detector(self) -> RepositoryDetector:
        return RepositoryDetectorImpl()
