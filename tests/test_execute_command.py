from nix_prefetch_github.effects import ExecuteCommand

from .markers import requires_nix_build
from .performer_test import performer_test


@performer_test
@requires_nix_build
def test_subprocess_stderr_is_captured(capsys):
    yield ExecuteCommand(
        ["nix-build", "does-not-exist-123-321"],
    )
    assert capsys.readouterr()[1]


@performer_test
@requires_nix_build
def test_subprocess_stderr_is_captured_when_merge_stderr_is_requested(capsys):
    yield ExecuteCommand(
        ["nix-build", "does-not-exist-123-321"],
    )
    assert capsys.readouterr()[1]
