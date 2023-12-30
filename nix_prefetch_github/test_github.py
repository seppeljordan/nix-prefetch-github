import logging
from datetime import datetime, timezone
from unittest import TestCase

from parameterized import parameterized

from nix_prefetch_github.github import GithubAPIImpl
from nix_prefetch_github.interfaces import GithubRepository
from nix_prefetch_github.tests import network


@network
class GithubTests(TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger()
        self.api = GithubAPIImpl(logger=self.logger)

    def test_that_for_own_repo_latest_release_is_not_none(self) -> None:
        self.assertIsNotNone(
            self.api.get_tag_of_latest_release(
                GithubRepository(
                    owner="seppeljordan",
                    name="nix-prefetch-github",
                )
            )
        )

    @parameterized.expand(
        [
            (
                "33285dcd1ee5850eccc0d620be7a03975b4ed2c0",
                datetime(2023, 12, 30, 14, 5, 55, tzinfo=timezone.utc),
            ),
            (
                "c2da1e1a6fb379285a34ca6458f01f372e28a24e",
                datetime(2023, 7, 9, 10, 6, 1, tzinfo=timezone.utc),
            ),
        ]
    )
    def test_that_for_own_repo_can_determin_the_commit_time_of_specific_commit(
        self, sha1: str, expected_datetime: datetime
    ) -> None:
        self.assertEqual(
            self.api.get_commit_date(
                GithubRepository(
                    owner="seppeljordan",
                    name="nix-prefetch-github",
                ),
                sha1,
            ),
            expected_datetime,
        )
