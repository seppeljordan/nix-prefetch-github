from io import StringIO
from unittest import TestCase

from .interfaces import PrefetchedRepository, PrefetchFailure, PrefetchOptions
from .presenter import Presenter
from .repository import GithubRepository


class PresenterTests(TestCase):
    def setUp(self) -> None:
        self.result_output = StringIO()
        self.error_output = StringIO()
        self.renderer = RepositoryRenderer()
        self.presenter = Presenter(
            result_output=self.result_output,
            error_output=self.error_output,
            repository_renderer=self.renderer,
        )
        self.repo = PrefetchedRepository(
            GithubRepository(owner="test", name="test"),
            rev="test",
            sha256="test",
            options=PrefetchOptions(),
        )

    def test_write_to_error_output_when_presenting_prefetch_failure(self) -> None:
        self.presenter.present(
            PrefetchFailure(reason=PrefetchFailure.Reason.unable_to_calculate_sha256)
        )
        self.assertTrue(self.read_error_output())

    def test_write_to_result_output_when_presenting_prefetched_repository(self) -> None:
        self.presenter.present(self.repo)
        self.assertTrue(self.read_result_output())

    def test_nothing_is_written_to_result_output_when_presenting_prefetch_failure(
        self,
    ) -> None:
        self.presenter.present(
            PrefetchFailure(reason=PrefetchFailure.Reason.unable_to_calculate_sha256)
        )
        self.assertFalse(self.read_result_output())

    def test_nothing_is_written_to_error_output_when_presenting_prefetched_respository(
        self,
    ) -> None:
        self.presenter.present(self.repo)
        self.assertFalse(self.read_error_output())

    def test_rendered_repository_is_writted_to_result_output(self) -> None:
        self.presenter.present(self.repo)
        self.assertIn(
            self.renderer.render_prefetched_repository(self.repo),
            self.read_result_output(),
        )

    def test_that_exit_0_is_returned_when_repository_is_rendered(self) -> None:
        return_code = self.presenter.present(self.repo)
        self.assertEqual(return_code, 0)

    def test_that_exit_1_is_returned_when_failure_is_rendered(self) -> None:
        return_code = self.presenter.present(
            PrefetchFailure(reason=PrefetchFailure.Reason.unable_to_calculate_sha256)
        )
        self.assertEqual(return_code, 1)

    def read_error_output(self) -> str:
        self.error_output.seek(0)
        return self.error_output.read()

    def read_result_output(self) -> str:
        self.result_output.seek(0)
        return self.result_output.read()


class RepositoryRenderer:
    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        return str(repository)
