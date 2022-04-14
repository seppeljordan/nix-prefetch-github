from logging import getLogger
from unittest import TestCase

from ..command.command_runner import CommandRunnerImpl
from ..interfaces import PrefetchOptions
from ..repository import GithubRepository
from ..tests import network, requires_nix_build
from .nix_prefetch import NixPrefetchUrlHasherImpl


@requires_nix_build
@network
class UrlHasherTests(TestCase):
    def setUp(self) -> None:
        self.hasher = NixPrefetchUrlHasherImpl(
            command_runner=CommandRunnerImpl(getLogger(__name__)), logger=getLogger()
        )
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

    def test_with_fetching_submodules(self) -> None:
        prefetch_options = PrefetchOptions(fetch_submodules=True)
        hash_sum = self.hasher.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertEqual(hash_sum, "wCo1YobyatxSOE85xQNSJw6jvufghFNHlZl4ToQjRHA=")

    def test_with_leaving_dotgit_dir(self) -> None:
        prefetch_options = PrefetchOptions(leave_dot_git=True)
        hash_sum = self.hasher.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertNotEqual(hash_sum, "B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM=")

    def test_with_deep_clone(self) -> None:
        # There is currently a bug in `nix-prefetch-git` that prevents
        # the UrlHasher under test to fail.  See
        # https://github.com/NixOS/nixpkgs/issues/168147 for details.
        # If this test passes then we can assume that we could swap
        # out the old implementation of UrlHasher with this one for
        # improved performance.
        prefetch_options = PrefetchOptions(deep_clone=True)
        hash_sum = self.hasher.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertEqual(hash_sum, "gBAtCILDbqofa6+9/bXR9drxymCGrgwf0+5mDxwF9p0=")
