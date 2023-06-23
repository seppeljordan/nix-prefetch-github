from logging import getLogger
from unittest import TestCase

from nix_prefetch_github.command.command_runner import CommandRunnerImpl
from nix_prefetch_github.hash_converter import HashConverterImpl
from nix_prefetch_github.tests import requires_nix_build


@requires_nix_build
class HashConverterTests(TestCase):
    def setUp(self) -> None:
        self.hash_converter = HashConverterImpl(
            command_runner=CommandRunnerImpl(logger=getLogger(__name__))
        )

    def test_return_none_if_input_is_not_a_valid_hash(self) -> None:
        assert self.hash_converter.convert_sha256_to_sri("abc") is None

    def test_return_sri_hash_if_hash_is_valid_sha256_hash(self) -> None:
        assert (
            self.hash_converter.convert_sha256_to_sri(
                "B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM="
            )
            == "sha256-B5AlNwg6kbcaqUiQEC6jslCRKVpErXLMsKC+b9aPlrM="
        )
