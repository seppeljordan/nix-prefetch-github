from unittest import TestCase

from nix_prefetch_github import GithubRepository
from nix_prefetch_github.url_hasher import PrefetchOptions, UrlHasherImpl
from tests.markers import network, requires_nix_build


@requires_nix_build
@network
class UrlHasherTests(TestCase):
    def setUp(self) -> None:
        self.hasher = UrlHasherImpl()
        self.repository = GithubRepository(
            owner="git-up",
            name="test-repo-submodules",
        )
        self.revision = "5a1dfa807759c39e3df891b6b46dfb2cf776c6ef"

    def test_without_fetching_submodules(self) -> None:
        prefetch_options = PrefetchOptions(fetch_submodules=False)
        hash_sum = self.hasher.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertEqual(hash_sum, "B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM=")

    def test_with_fetching_submosules(self) -> None:
        prefetch_options = PrefetchOptions(fetch_submodules=True)
        hash_sum = self.hasher.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertEqual(hash_sum, "wCo1YobyatxSOE85xQNSJw6jvufghFNHlZl4ToQjRHA=")
