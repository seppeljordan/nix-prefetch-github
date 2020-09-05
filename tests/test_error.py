import pytest

from nix_prefetch_github.core import GithubRepository, revision_not_found_errormessage


@pytest.fixture
def repository():
    return GithubRepository(owner="test_owner", name="test_repo")


@pytest.fixture
def revision_not_found_message(repository):
    return revision_not_found_errormessage(
        repository=repository, revision="test_revision"
    )


def test_revision_not_found_errormessage_is_a_string(revision_not_found_message):
    assert isinstance(revision_not_found_message, str)


def test_revision_not_found_errormessage_contains_owner_repo_and_revision(
    revision_not_found_message,
):
    assert "test_owner" in revision_not_found_message
    assert "test_repo" in revision_not_found_message
    assert "test_revision" in revision_not_found_message
