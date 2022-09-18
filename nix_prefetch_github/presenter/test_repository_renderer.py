from typing import List
from unittest import TestCase

from nix_prefetch_github.interfaces import (
    GithubRepository,
    PrefetchedRepository,
    PrefetchOptions,
    RepositoryRenderer,
)
from nix_prefetch_github.presenter.repository_renderer import (
    JsonRepositoryRenderer,
    NixRepositoryRenderer,
)


class GeneralRepositoryRendererTests(TestCase):
    def setUp(self) -> None:
        self.renderers: List[RepositoryRenderer] = [
            NixRepositoryRenderer(),
            JsonRepositoryRenderer(),
        ]

    def test_that_rendering_prefetched_repo_with_and_without_dot_git_directory_produces_different_output(
        self,
    ) -> None:
        for renderer in self.renderers:
            with self.subTest():
                without_dot_git = self._make_repository(leave_dot_git=False)
                with_dot_git = self._make_repository(leave_dot_git=True)
                self.assertNotEqual(
                    renderer.render_prefetched_repository(without_dot_git),
                    renderer.render_prefetched_repository(with_dot_git),
                )

    def test_that_rendering_prefetched_repo_with_and_without_deep_clone_produces_different_output(
        self,
    ) -> None:
        renderers: List[RepositoryRenderer] = [
            NixRepositoryRenderer(),
            JsonRepositoryRenderer(),
        ]
        for renderer in renderers:
            with self.subTest():
                without_deep_clone = self._make_repository(deep_clone=False)
                with_deep_clone = self._make_repository(deep_clone=True)
                self.assertNotEqual(
                    renderer.render_prefetched_repository(without_deep_clone),
                    renderer.render_prefetched_repository(with_deep_clone),
                )

    def _make_repository(
        self, leave_dot_git: bool = False, deep_clone: bool = False
    ) -> PrefetchedRepository:
        return PrefetchedRepository(
            repository=GithubRepository(owner="test", name="test"),
            rev="test",
            sha256="test",
            options=PrefetchOptions(leave_dot_git=leave_dot_git, deep_clone=deep_clone),
        )
