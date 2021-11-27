from logging import Logger, getLogger

from .core import RevisionIndexFactory, UrlHasher
from .remote_list_factory import RemoteListFactoryImpl
from .revision_index import RemoteListFactory, RevisionIndexFactoryImpl
from .url_hasher import UrlHasherImpl


class DependencyInjector:
    def get_revision_index_factory(self) -> RevisionIndexFactory:
        return RevisionIndexFactoryImpl(
            self.get_remote_list_factory(), self.get_logger()
        )

    def get_remote_list_factory(self) -> RemoteListFactory:
        return RemoteListFactoryImpl()

    def get_logger(self) -> Logger:
        return getLogger()

    def get_url_hasher(self) -> UrlHasher:
        return UrlHasherImpl()
