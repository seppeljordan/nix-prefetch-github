from nix_prefetch_github.interfaces import (
    GithubRepository,
    PrefetchedRepository,
    PrefetchOptions,
    RenderingFormat,
)
from nix_prefetch_github.tests import BaseTestCase

from .repository_renderer import RenderingSelectorImpl


class RenderingSelectorImplTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.nix_renderer = RepositoryRendererImpl("nix format")
        self.json_renderer = RepositoryRendererImpl("json format")
        self.rendering_selector = RenderingSelectorImpl(
            nix_renderer=self.nix_renderer,
            json_renderer=self.json_renderer,
        )

    def test_by_default_json_format_is_selectored(self) -> None:
        output = self.rendering_selector.render_prefetched_repository(
            self.get_repository()
        )
        self.assertEqual(output, "json format")

    def test_that_output_format_is_nix_after_nix_output_was_selected(self) -> None:
        self.rendering_selector.set_rendering_format(RenderingFormat.nix)
        output = self.rendering_selector.render_prefetched_repository(
            self.get_repository()
        )
        self.assertEqual(output, "nix format")

    def test_that_output_format_is_json_after_json_output_was_selected(self) -> None:
        self.rendering_selector.set_rendering_format(RenderingFormat.json)
        output = self.rendering_selector.render_prefetched_repository(
            self.get_repository()
        )
        self.assertEqual(output, "json format")

    def test_that_output_of_json_renderer_is_respected(self) -> None:
        self.json_renderer.output = "json format 2"
        output = self.rendering_selector.render_prefetched_repository(
            self.get_repository()
        )
        self.assertEqual(output, "json format 2")

    def test_that_output_of_nix_renderer_is_respected(self) -> None:
        self.rendering_selector.set_rendering_format(RenderingFormat.nix)
        self.nix_renderer.output = "nix format 2"
        output = self.rendering_selector.render_prefetched_repository(
            self.get_repository()
        )
        self.assertEqual(output, "nix format 2")

    def get_repository(self) -> PrefetchedRepository:
        return PrefetchedRepository(
            repository=GithubRepository(owner="test", name="test"),
            hash_sum="",
            options=PrefetchOptions(),
            rev="",
        )


class RepositoryRendererImpl:
    def __init__(self, output: str) -> None:
        self.output = output

    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        return self.output
