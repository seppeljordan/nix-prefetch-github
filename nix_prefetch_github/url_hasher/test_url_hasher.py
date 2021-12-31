from logging import getLogger
from unittest import TestCase

from ..command import CommandRunner
from ..repository import GithubRepository
from ..tests import network, requires_nix_build
from . import PrefetchOptions, UrlHasherImpl, detect_actual_hash_from_nix_output


@requires_nix_build
@network
class UrlHasherTests(TestCase):
    def setUp(self) -> None:
        self.hasher = UrlHasherImpl(command_runner=CommandRunner(getLogger(__name__)))
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
        prefetch_options = PrefetchOptions(deep_clone=True)
        hash_sum = self.hasher.calculate_sha256_sum(
            repository=self.repository,
            revision=self.revision,
            prefetch_options=prefetch_options,
        )
        self.assertNotEqual(hash_sum, "B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM=")


class DetectActualHashFromNixOutputTests(TestCase):
    def setUp(self) -> None:
        self.data = (
            (
                [
                    "hash mismatch in fixed-output derivation '/nix/store/7pzdkrl1ddw9blkr4jymwavbxmxxdwm1-source':",
                    "  wanted: sha256:1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv",
                    "  got:    sha256:0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6",
                    "error: build of '/nix/store/rfjcq0fcmiz7masslf7q27xs012v6mnp-source.drv' failed",
                ],
                "0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6",
            ),
            (
                [
                    "fixed-output derivation produced path '/nix/store/cn22m5wz95whqi4wgzfw5cfz9knslak4-source' with sha256 hash '0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6' instead of the expected hash '0401067152dx9z878d4l6dryy7f611g2bm8rq4dyn366w6c9yrcb'",
                    "cannot build derivation '/nix/store/8savxwnx8yw7r1ccrc00l680lmq5c15f-output.drv': 1 dependencies couldn't be built",
                ],
                "0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6",
            ),
            (
                [
                    "output path '/nix/store/z9zpz2yqx1ixn4xl1lsrk0f83rvp7srb-source' has r:sha256 hash '0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6' when '1mkcnzy1cfpwghgvb9pszhy9jy6534y8krw8inwl9fqfd0w019wz' was expected"
                ],
                "0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6",
            ),
            (
                [
                    "  specified: sha256-u42evoAl/P3/Ad6lcXgS1+dd2fcBwEqu4gNU/OjxlPg=",
                    "     got:    sha256-66Ynq+4sh59apqAEVeVLIAxkFgy96QSdpQjsLlsGoNo=",
                ],
                "66Ynq+4sh59apqAEVeVLIAxkFgy96QSdpQjsLlsGoNo=",
            ),
        )

    def test_that_detect_actual_hash_from_nix_output_works_for_multiple_version_of_nix(
        self,
    ) -> None:
        # This test checks if the nix-prefetch-github is compatible with
        # different versions of nix
        for nix_build_output, actual_hash in self.data:
            with self.subTest():
                detected_hash = detect_actual_hash_from_nix_output(nix_build_output)
                self.assertEqual(detected_hash, actual_hash)
