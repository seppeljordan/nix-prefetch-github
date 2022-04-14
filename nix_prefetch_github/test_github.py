from unittest import TestCase

from .github import GithubAPIImpl
from .interfaces import GithubRepository
from .tests import network


@network
class GithubTests(TestCase):
    def setUp(self) -> None:
        self.api = GithubAPIImpl()

    def test_that_for_own_repo_latest_release_is_not_none(self) -> None:
        self.assertIsNotNone(
            self.api.get_tag_of_latest_release(
                GithubRepository(
                    owner="seppeljordan",
                    name="nix-prefetch-github",
                )
            )
        )
