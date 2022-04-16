from typing import Optional
from unittest import TestCase

from nix_prefetch_github.interfaces import GithubRepository
from nix_prefetch_github.list_remote import ListRemote
from nix_prefetch_github.revision_index import RevisionIndexImpl
from nix_prefetch_github.revision_index_factory import RevisionIndexFactoryImpl


class FakeListRemoteFactory:
    def __init__(self) -> None:
        self.remote: Optional[ListRemote] = None

    def get_list_remote(self, repository: GithubRepository) -> Optional[ListRemote]:
        return self.remote


class RevisionIndexFactoryTests(TestCase):
    def setUp(self) -> None:
        self.repository = GithubRepository(owner="test owner", name="test name")
        self.list_remote_factory = FakeListRemoteFactory()
        self.revision_index_factory = RevisionIndexFactoryImpl(self.list_remote_factory)

    def set_list_remote(self, list_remote: Optional[ListRemote]) -> None:
        self.list_remote_factory.remote = list_remote

    def test_list_remote_factory_returns_none_then_revision_index_factory_also_returns_none(
        self,
    ) -> None:
        self.set_list_remote(None)
        self.assertIsNone(
            self.revision_index_factory.get_revision_index(self.repository)
        )

    def test_list_remote_facory_returns_a_remote_then_revision_index_factory_returns_a_revision(
        self,
    ) -> None:
        self.set_list_remote(ListRemote())
        self.assertIsInstance(
            self.revision_index_factory.get_revision_index(self.repository),
            RevisionIndexImpl,
        )
