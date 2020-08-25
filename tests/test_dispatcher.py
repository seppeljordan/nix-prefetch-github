from effect import Effect

from nix_prefetch_github.core import GetListRemote
from nix_prefetch_github.effect import perform_effects

from .markers import network


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
