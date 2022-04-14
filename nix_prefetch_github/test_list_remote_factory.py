from logging import getLogger
from unittest import TestCase

from .command.command_runner import CommandRunnerImpl
from .list_remote_factory import ListRemoteFactoryImpl
from .repository import GithubRepository
from .tests import network


@network
class RemoteListFactoryTests(TestCase):
    def setUp(self) -> None:
        self.factory = ListRemoteFactoryImpl(
            command_runner=CommandRunnerImpl(getLogger(__name__))
        )

    def test_for_non_existing_repo_we_get_none(self) -> None:
        repository = GithubRepository(
            owner="seppeljordan", name="repo_does_not_exist_12653"
        )
        remote_list = self.factory.get_list_remote(repository)
        self.assertIsNone(remote_list)

    def test_for_existing_repository_we_get_truthy_value(self) -> None:
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        remote_list = self.factory.get_list_remote(repository)
        self.assertTrue(remote_list)

    def test_get_correct_reference_for_version_v2_3(self) -> None:
        repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
        remote_list = self.factory.get_list_remote(repository)
        assert remote_list
        self.assertEqual(
            remote_list.tag("v2.3"), "e632ce77435a4ab269c227c3ebcbaeaf746f8627"
        )
