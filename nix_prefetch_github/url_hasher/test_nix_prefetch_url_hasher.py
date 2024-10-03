from logging import getLogger
from unittest import TestCase

from parameterized import parameterized

from nix_prefetch_github.command.command_runner import CommandRunnerImpl
from nix_prefetch_github.hash_converter import HashConverterImpl
from nix_prefetch_github.interfaces import GithubRepository, PrefetchOptions
from nix_prefetch_github.tests import CommandRunnerTestImpl, network
from nix_prefetch_github.url_hasher.nix_prefetch import NixPrefetchUrlHasherImpl


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

    @parameterized.expand(
        [
            (
                "git-up",
                "test-repo-submodules",
                "5a1dfa807759c39e3df891b6b46dfb2cf776c6ef",
                PrefetchOptions(),
                "sha256-B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM=",
                "/nix/store/d9bp6cchg2scyjfqnpxh7ghmw6fjmxvf-5a1dfa807759c39e3df891b6b46dfb2cf776c6ef.tar.gz",
            ),
            (
                "git-up",
                "test-repo-submodules",
                "5a1dfa807759c39e3df891b6b46dfb2cf776c6ef",
                PrefetchOptions(fetch_submodules=True),
                "sha256-wCo1YobyatxSOE85xQNSJw6jvufghFNHlZl4ToQjRHA=",
                "/nix/store/5zb52kqrzvyc2na8lprv8vnky5fjw8f3-test-repo-submodules-5a1dfa8",
            ),
            (
                "git-up",
                "test-repo-submodules",
                "5a1dfa807759c39e3df891b6b46dfb2cf776c6ef",
                PrefetchOptions(leave_dot_git=True),
                "sha256-0Za18NiCiPL9KFG4OzgIsM11bXOeRofKoEHgScvlEQg=",
                "/nix/store/rx3yji4dpkqzqb60zxp9rz8ql8sxwd60-test-repo-submodules-5a1dfa8",
            ),
            (
                "seppeljordan",
                "nix-prefetch-github",
                "9578399cadb1cb2b252438cf14663333e8c3ee00",
                PrefetchOptions(),
                "sha256-JFC1+y+FMs2TwWjJxlAKAyDbSLFBE9J65myp7+slp50=",
                "/nix/store/6wv3zc015amj7mc9krffskj447xyajf6-9578399cadb1cb2b252438cf14663333e8c3ee00.tar.gz",
            ),
            (
                "seppeljordan",
                "nix-prefetch-github",
                "9578399cadb1cb2b252438cf14663333e8c3ee00",
                PrefetchOptions(fetch_submodules=True),
                "sha256-JFC1+y+FMs2TwWjJxlAKAyDbSLFBE9J65myp7+slp50=",
                "/nix/store/dsfrwkrjjlsnydb8blph0gxr7p0xbnlm-nix-prefetch-github-9578399",
            ),
        ]
    )
    def test_well_known_configurations_for_their_expected_hashes_and_store_paths(
        self,
        owner: str,
        repo: str,
        revision: str,
        options: PrefetchOptions,
        expected_hash_sum: str,
        expected_store_path: str,
    ) -> None:
        prefetched_repo = self.hasher.calculate_hash_sum(
            repository=GithubRepository(owner=owner, name=repo),
            revision=revision,
            prefetch_options=options,
        )
        assert prefetched_repo
        self.assertEqual(prefetched_repo.hash_sum, expected_hash_sum)
        self.assertEqual(prefetched_repo.store_path, expected_store_path)

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

    def test_with_deep_clone(self) -> None:
        prefetch_options = PrefetchOptions(deep_clone=True)
        prefetched_repo = self.hasher.calculate_hash_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        assert prefetched_repo
