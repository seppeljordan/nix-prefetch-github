import subprocess

from effect import Effect
from pytest import fixture, raises

from nix_prefetch_github.core import (
    CheckGitRepoIsDirty,
    GetListRemote,
    GetRevisionForLatestRelease,
    GithubRepository,
    ShowWarning,
    TryPrefetch,
    is_sha1_hash,
)
from nix_prefetch_github.effects import perform_effects

from .markers import network, requires_nix_build


@network
def test_get_list_remote_retrieves_correct_tags():
    repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
    remote = perform_effects(Effect(GetListRemote(repository=repository)))
    assert remote.tag("v2.3") == "e632ce77435a4ab269c227c3ebcbaeaf746f8627"


@network
def test_get_list_remote_returns_none_for_none_existing_repos():
    repository = GithubRepository(owner="seppeljordan", name="non-existing-repo-123")
    with raises(SystemExit):
        perform_effects(Effect(GetListRemote(repository=repository)))


@network
@requires_nix_build
def test_try_prefetch_returns_errorcode_when_fetching_with_invalid_sha256():
    repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
    returncode, _ = perform_effects(
        Effect(
            TryPrefetch(
                repository=repository,
                sha256="abc",
                rev="e632ce77435a4ab269c227c3ebcbaeaf746f8627",
                fetch_submodules=True,
            )
        )
    )
    assert returncode


@network
@requires_nix_build
def test_try_prefetch_actually_fetches_proper_commits_with_correct_hash():
    repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
    returncode, _ = perform_effects(
        Effect(
            TryPrefetch(
                repository=repository,
                sha256="sAXKffNUTfepcMfgOZahs7hofkMpsxI9NRhT2L17UCw=",
                rev="e632ce77435a4ab269c227c3ebcbaeaf746f8627",
                fetch_submodules=True,
            )
        )
    )
    assert not returncode


@network
def test_get_latest_revision():
    repository = GithubRepository(owner="seppeljordan", name="nix-prefetch-github")
    revision_hash = perform_effects(
        Effect(GetRevisionForLatestRelease(repository=repository))
    )
    assert is_sha1_hash(revision_hash)


@network
def test_get_revision_for_latest_release_raises_HTTPError_when_repo_not_found():
    repository = GithubRepository(
        owner="seppeljordan", name="repository-does-not-exist"
    )
    commit = perform_effects(Effect(GetRevisionForLatestRelease(repository=repository)))
    assert not commit


def test_show_warning(capsys):
    perform_effects(Effect(ShowWarning(message="test message")))
    captured = capsys.readouterr()
    assert "WARNING" in captured.err
    assert "test message" in captured.err


def test_check_git_repo_is_dirty_raises_on_empty_repositories(empty_git_repo):
    with raises(Exception):
        perform_effects(Effect(CheckGitRepoIsDirty(directory=empty_git_repo)))


def test_check_git_repo_is_dirty_works_on_clean_repos(empty_git_repo):
    subprocess.run(["touch", "test.txt"], cwd=empty_git_repo)
    subprocess.run(["git", "add", "test.txt"], cwd=empty_git_repo)
    subprocess.run(["git", "commit", "-a", "-m" "test commit"], cwd=empty_git_repo)
    is_dirty = perform_effects(Effect(CheckGitRepoIsDirty(directory=empty_git_repo)))
    assert not is_dirty


def test_check_git_repo_is_dirty_works_on_dirty_repos(empty_git_repo):
    subprocess.run(["touch", "test.txt"], cwd=empty_git_repo)
    subprocess.run(["git", "add", "test.txt"], cwd=empty_git_repo)
    subprocess.run(["git", "commit", "-a", "-m" "test commit"], cwd=empty_git_repo)
    subprocess.run(["touch", "test2.txt"], cwd=empty_git_repo)
    subprocess.run(["git", "add", "test2.txt"], cwd=empty_git_repo)
    is_dirty = perform_effects(Effect(CheckGitRepoIsDirty(directory=empty_git_repo)))
    assert is_dirty


@fixture
def empty_git_repo(tmpdir):
    subprocess.run(["git", "init"], cwd=tmpdir)
    subprocess.run(["git", "config", "user.name", "test user"], cwd=tmpdir)
    subprocess.run(["git", "config", "user.email", "test@email.test"], cwd=tmpdir)

    return tmpdir
