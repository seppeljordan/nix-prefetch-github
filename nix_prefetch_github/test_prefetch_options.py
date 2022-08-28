from unittest import TestCase

from nix_prefetch_github.interfaces import PrefetchOptions


class PrefetchOptionsTests(TestCase):
    def test_that_default_options_are_considered_safe(self) -> None:
        options = PrefetchOptions()
        self.assertTrue(options.is_safe())

    def test_that_deep_clone_is_not_considered_safe(self) -> None:
        options = PrefetchOptions(deep_clone=True)
        self.assertFalse(options.is_safe())

    def test_that_leave_dot_git_is_not_considered_safe(self) -> None:
        options = PrefetchOptions(leave_dot_git=True)
        self.assertFalse(options.is_safe())
