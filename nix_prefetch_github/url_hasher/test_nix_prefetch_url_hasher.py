from logging import getLogger
from unittest import TestCase

from nix_prefetch_github.command.command_runner import CommandRunnerImpl
from nix_prefetch_github.hash_converter import HashConverterImpl
from nix_prefetch_github.interfaces import GithubRepository, PrefetchOptions
from nix_prefetch_github.tests import CommandRunnerTestImpl, network, requires_nix_build
from nix_prefetch_github.url_hasher.nix_prefetch import NixPrefetchUrlHasherImpl


@requires_nix_build
@network
class UrlHasherTests(TestCase):
    def setUp(self) -> None:
        self.command_runner = CommandRunnerTestImpl(
            command_runner=CommandRunnerImpl(getLogger(__name__))
        )
        hash_converter = HashConverterImpl(command_runner=self.command_runner)
        self.hasher = NixPrefetchUrlHasherImpl(
            command_runner=self.command_runner,
            logger=getLogger(),
            hash_converter=hash_converter,
        )
        self.repository = GithubRepository(
            owner="git-up",
            name="test-repo-submodules",
        )
        self.revision = "5a1dfa807759c39e3df891b6b46dfb2cf776c6ef"

    def test_without_fetching_submodules(self) -> None:
        prefetch_options = PrefetchOptions(fetch_submodules=False)
        hash_sum = self.hasher.calculate_hash_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertEqual(
            hash_sum, "sha256-B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM="
        )

    def test_that_experimental_feature_nix_command_is_enabled(self) -> None:
        self.hasher.calculate_hash_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=PrefetchOptions(),
        )
        issued_nix_commands = list(
            filter(lambda c: c[0] == "nix", self.command_runner.commands_issued)
        )
        self.assertTrue(
            all(
                command[1] == "--extra-experimental-features"
                and command[2] == "nix-command"
                for command in issued_nix_commands
            ),
            msg="Not all commands in  %s do include '--extra-experimental-features nix-command'"
            % issued_nix_commands,
        )

    def test_with_fetching_submodules(self) -> None:
        prefetch_options = PrefetchOptions(fetch_submodules=True)
        hash_sum = self.hasher.calculate_hash_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertEqual(
            hash_sum, "sha256-wCo1YobyatxSOE85xQNSJw6jvufghFNHlZl4ToQjRHA="
        )

    def test_with_leaving_dotgit_dir(self) -> None:
        prefetch_options = PrefetchOptions(leave_dot_git=True)
        hash_sum = self.hasher.calculate_hash_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertNotEqual(
            hash_sum, "sha256-B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM="
        )

    def test_with_deep_clone(self) -> None:
        prefetch_options = PrefetchOptions(deep_clone=True)
        hash_sum = self.hasher.calculate_hash_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertEqual(
            hash_sum, "sha256-gBAtCILDbqofa6+9/bXR9drxymCGrgwf0+5mDxwF9p0="
        )
