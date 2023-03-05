from unittest import TestCase

from nix_prefetch_github.hash import SriHash


class SriHashTests(TestCase):
    def test_that_hash_function_and_digest_can_be_extracted_from_valid_sri_hashes(
        self,
    ) -> None:
        examples = [
            (
                "sha384-H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO",
                "sha384",
                "H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO",
            ),
            (
                "sha512-Q2bFTOhEALkN8hOms2FKTDLy7eugP2zFZ1T8LCvX42Fp3WoNr3bjZSAHeOsHrbV1Fu9/A0EzCinRE7Af1ofPrw==",
                "sha512",
                "Q2bFTOhEALkN8hOms2FKTDLy7eugP2zFZ1T8LCvX42Fp3WoNr3bjZSAHeOsHrbV1Fu9/A0EzCinRE7Af1ofPrw==",
            ),
            (
                "sha384-H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO?fakeoption",
                "sha384",
                "H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO",
            ),
        ]
        for example, expected_algorithm, expected_digest in examples:
            with self.subTest(example):
                sri = SriHash.from_text(example)
                assert sri.hash_function == expected_algorithm
                assert sri.digest == expected_digest

    def test_that_options_are_extracted_from_valid_hashes(self) -> None:
        examples = [
            (
                "sha384-H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO",
                [],
            ),
            (
                "sha384-H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO?fakeoption",
                ["fakeoption"],
            ),
        ]
        for example, expected_options in examples:
            with self.subTest(example):
                sri = SriHash.from_text(example)
                assert expected_options == sri.options

    def test_that_hash_with_options_can_be_displayed_correctly(self) -> None:
        examples = [
            "sha384-H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO",
            "sha384-H8BRh8j48O9oYatfu5AZzq6A9RINhZO5H16dQZngK7T62em8MUt1FLm52t+eX6xO?fakeoption",
        ]
        for example in examples:
            with self.subTest(example):
                sri = SriHash.from_text(example)
                assert str(sri) == example

    def test_that_with_invalid_format_raise_value_error(self) -> None:
        examples = [
            "",
            "abc",
        ]
        for example in examples:
            with self.subTest(example):
                with self.assertRaises(ValueError):
                    SriHash.from_text(example)
