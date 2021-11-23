import subprocess
from tempfile import TemporaryDirectory
from unittest import TestCase

from ..tests import network, requires_nix_build
from . import nix_prefetch_github


@requires_nix_build
@network
class NixPrefetchGithubTests(TestCase):
    def test_life_mode(self):
        results = nix_prefetch_github(
            owner="seppeljordan", repo="pypi2nix", prefetch=True, rev=None
        )
        self.assertTrue(results.sha256)

    def test_to_nix_expression_outputs_valid_nix_expr(self):
        for prefetch in [False, True]:
            prefetched_repository = nix_prefetch_github(
                owner="seppeljordan",
                repo="pypi2nix",
                prefetch=prefetch,
                rev="master",
                fetch_submodules=True,
            )
            nix_expr_output = prefetched_repository.to_nix_expression()

            with TemporaryDirectory() as temp_dir_name:
                nix_filename = temp_dir_name + "/output.nix"
                with open(nix_filename, "w") as f:
                    f.write(nix_expr_output)
                completed_process = subprocess.run(
                    ["nix-build", nix_filename, "--no-out-link"]
                )
                self.assertEqual(completed_process.returncode, 0)
