from unittest import TestCase

from .core import GithubRepository
from .remote_list_factory import RemoteListFactoryImpl
from .tests import network


@network
class RemoteListFactoryTests(TestCase):
    def setUp(self) -> None:
        self.factory = RemoteListFactoryImpl()

    def test_for_non_existing_repo_we_get_none(self) -> None:
        repository = GithubRepository(
            owner="seppeljordan", name="repo_does_not_exist_12653"
        )
        remote_list = self.factory.get_remote_list(repository)
        self.assertIsNone(remote_list)

    def test_for_existing_repository_we_get_truthy_value(self) -> None:
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        remote_list = self.factory.get_remote_list(repository)
        self.assertTrue(remote_list)

    def test_get_correct_reference_for_version_v2_3(self) -> None:
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        remote_list = self.factory.get_remote_list(repository)
        assert remote_list
        self.assertEqual(
            remote_list.tag("v2.3"), "e632ce77435a4ab269c227c3ebcbaeaf746f8627"
        )
