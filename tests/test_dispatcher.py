from effect import Effect

from nix_prefetch_github.core import GetListRemote, TryPrefetch
from nix_prefetch_github.effect import perform_effects

from .markers import network, requires_nix_build


@network
def test_get_list_remote_retrieves_correct_tags():
    remote = perform_effects(
        Effect(GetListRemote(owner="seppeljordan", repo="nix-prefetch-github"))
    )
    assert remote.tag("v2.3") == "e632ce77435a4ab269c227c3ebcbaeaf746f8627"


@network
def test_get_list_remote_returns_none_for_none_existing_repos():
    remote = perform_effects(
        Effect(GetListRemote(owner="seppeljordan", repo="non-existing-repo-123"))
    )
    assert not remote


@network
@requires_nix_build
def test_try_prefetch_returns_errorcode_when_fetching_with_invalid_sha256():
    returncode, _ = perform_effects(
        Effect(
            TryPrefetch(
                owner="seppeljordan",
                repo="nix-prefetch-github",
                sha256="abc",
                rev="e632ce77435a4ab269c227c3ebcbaeaf746f8627",
            )
        )
    )
    assert returncode


@network
@requires_nix_build
def test_try_prefetch():
    returncode, _ = perform_effects(
        Effect(
            TryPrefetch(
                owner="seppeljordan",
                repo="nix-prefetch-github",
                sha256="sha256-sAXKffNUTfepcMfgOZahs7hofkMpsxI9NRhT2L17UCw=",
                rev="e632ce77435a4ab269c227c3ebcbaeaf746f8627",
            )
        )
    )
    assert not returncode
