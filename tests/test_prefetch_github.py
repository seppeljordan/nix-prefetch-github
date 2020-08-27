import subprocess
from tempfile import TemporaryDirectory

import pytest
from effect.testing import perform_sequence

import nix_prefetch_github
from nix_prefetch_github import ListRemote
from nix_prefetch_github.core import (
    AbortWithErrorMessage,
    revision_not_found_errormessage,
)

from .markers import network, requires_nix_build


@pytest.fixture
def pypi2nix_list_remote():
    return ListRemote.from_git_ls_remote_output(
        "\n".join(
            [
                "ref: refs/heads/master\tHEAD",
                "1234\trefs/heads/dev",
                "5678\trefs/heads/master",
                "1234\trefs/tags/v1.0",
            ]
        )
    )


def test_prefetch_github_actual_prefetch(pypi2nix_list_remote):
    seq = [
        (
            nix_prefetch_github.GetListRemote(owner="seppeljordan", repo="pypi2nix"),
            lambda i: pypi2nix_list_remote,
        ),
        (
            nix_prefetch_github.CalculateSha256Sum(
                owner="seppeljordan",
                repo="pypi2nix",
                revision=pypi2nix_list_remote.branch("master"),
            ),
            lambda i: "TEST_ACTUALHASH",
        ),
        (
            nix_prefetch_github.TryPrefetch(
                owner="seppeljordan",
                repo="pypi2nix",
                rev=pypi2nix_list_remote.branch("master"),
                sha256="TEST_ACTUALHASH",
            ),
            lambda i: None,
        ),
    ]
    eff = nix_prefetch_github.prefetch_github(
        owner="seppeljordan", repo="pypi2nix", prefetch=True
    )
    prefetch_result = perform_sequence(seq, eff)
    assert prefetch_result.rev == pypi2nix_list_remote.branch("master")
    assert prefetch_result.sha256 == "TEST_ACTUALHASH"


def test_can_prefetch_from_tag_given_as_rev(pypi2nix_list_remote):
    seq = [
        (
            nix_prefetch_github.GetListRemote(owner="seppeljordan", repo="pypi2nix"),
            lambda i: pypi2nix_list_remote,
        ),
        (
            nix_prefetch_github.CalculateSha256Sum(
                owner="seppeljordan",
                repo="pypi2nix",
                revision=pypi2nix_list_remote.tag("v1.0"),
            ),
            lambda i: "TEST_ACTUALHASH",
        ),
    ]
    eff = nix_prefetch_github.prefetch_github(
        owner="seppeljordan", repo="pypi2nix", prefetch=False, rev="v1.0"
    )
    prefetch_result = perform_sequence(seq, eff)
    assert prefetch_result.rev == pypi2nix_list_remote.tag("v1.0")
    assert prefetch_result.sha256 == "TEST_ACTUALHASH"


def test_prefetch_github_no_actual_prefetch(pypi2nix_list_remote):
    seq = [
        (
            nix_prefetch_github.GetListRemote(owner="seppeljordan", repo="pypi2nix"),
            lambda i: pypi2nix_list_remote,
        ),
        (
            nix_prefetch_github.CalculateSha256Sum(
                owner="seppeljordan",
                repo="pypi2nix",
                revision=pypi2nix_list_remote.branch("master"),
            ),
            lambda i: "TEST_ACTUALHASH",
        ),
    ]
    eff = nix_prefetch_github.prefetch_github(
        owner="seppeljordan", repo="pypi2nix", prefetch=False
    )
    prefetch_result = perform_sequence(seq, eff)
    assert prefetch_result.rev == pypi2nix_list_remote.branch("master")
    assert prefetch_result.sha256 == "TEST_ACTUALHASH"


def test_prefetch_github_rev_given():
    commit_hash = "50553a665d2700c353ac41ab28c23b1027b7c1f0"
    seq = [
        (
            nix_prefetch_github.CalculateSha256Sum(
                owner="seppeljordan", repo="pypi2nix", revision=commit_hash
            ),
            lambda i: "TEST_ACTUALHASH",
        )
    ]
    eff = nix_prefetch_github.prefetch_github(
        owner="seppeljordan", repo="pypi2nix", prefetch=False, rev=commit_hash
    )
    prefetch_result = perform_sequence(seq, eff)
    assert prefetch_result.rev == commit_hash
    assert prefetch_result.sha256 == "TEST_ACTUALHASH"


def test_prefetch_aborts_when_rev_is_not_found(pypi2nix_list_remote):
    sequence = [
        (
            nix_prefetch_github.GetListRemote(owner="seppeljordan", repo="pypi2nix"),
            lambda _: pypi2nix_list_remote,
        ),
        (
            AbortWithErrorMessage(
                revision_not_found_errormessage(
                    owner="seppeljordan", repo="pypi2nix", revision="does-not-exist"
                )
            ),
            lambda _: None,
        ),
    ]
    effect = nix_prefetch_github.prefetch_github(
        owner="seppeljordan", repo="pypi2nix", rev="does-not-exist"
    )
    prefetch_result = perform_sequence(sequence, effect)
    assert prefetch_result is None


@requires_nix_build
@network
def test_life_mode():
    results = nix_prefetch_github.nix_prefetch_github(
        owner="seppeljordan", repo="pypi2nix", prefetch=True, rev=None
    )
    assert results.sha256


def test_is_sha1_hash_detects_actual_hash():
    text = "5a484700f1006389847683a72cd88bf7057fe772"
    assert nix_prefetch_github.is_sha1_hash(text)


def test_is_sha1_hash_returns_false_for_string_to_short():
    text = "5a484700f1006389847683a72cd88bf7057fe77"
    assert len(text) < 40
    assert not nix_prefetch_github.is_sha1_hash(text)


@requires_nix_build
@network
def test_to_nix_expression_outputs_valid_nix_expr():
    for prefetch in [False, True]:
        prefetched_repository = nix_prefetch_github.nix_prefetch_github(
            owner="seppeljordan",
            repo="pypi2nix",
            prefetch=prefetch,
            rev="master",
            fetch_submodules=False,
        )
        nix_expr_output = prefetched_repository.to_nix_expression()

        with TemporaryDirectory() as temp_dir_name:
            nix_filename = temp_dir_name + "/output.nix"
            with open(nix_filename, "w") as f:
                f.write(nix_expr_output)
            completed_process = subprocess.run(
                ["nix-build", nix_filename, "--no-out-link"]
            )
            assert completed_process.returncode == 0


@pytest.mark.parametrize(
    "nix_build_output",
    (
        [
            "hash mismatch in fixed-output derivation '/nix/store/7pzdkrl1ddw9blkr4jymwavbxmxxdwm1-source':",
            "  wanted: sha256:1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv",
            "  got:    sha256:0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6",
            "error: build of '/nix/store/rfjcq0fcmiz7masslf7q27xs012v6mnp-source.drv' failed",
        ],
        [
            "fixed-output derivation produced path '/nix/store/cn22m5wz95whqi4wgzfw5cfz9knslak4-source' with sha256 hash '0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6' instead of the expected hash '0401067152dx9z878d4l6dryy7f611g2bm8rq4dyn366w6c9yrcb'",
            "cannot build derivation '/nix/store/8savxwnx8yw7r1ccrc00l680lmq5c15f-output.drv': 1 dependencies couldn't be built",
        ],
        [
            "output path '/nix/store/z9zpz2yqx1ixn4xl1lsrk0f83rvp7srb-source' has r:sha256 hash '0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6' when '1mkcnzy1cfpwghgvb9pszhy9jy6534y8krw8inwl9fqfd0w019wz' was expected"
        ],
    ),
)
def test_that_detect_actual_hash_from_nix_output_works_for_multiple_version_of_nix(
    nix_build_output,
):
    # This test checks if the nix-prefetch-github is compatible with
    # different versions of nix
    actual_sha256_hash = "0x1x9dq4hnkdrdfbvcm6kaivrkgmmr4vp2qqwz15y5pcawvyd0z6"
    assert actual_sha256_hash == nix_prefetch_github.detect_actual_hash_from_nix_output(
        nix_build_output
    )


def test_that_prefetch_github_understands_full_ref_names(pypi2nix_list_remote):
    sequence = [
        (
            nix_prefetch_github.GetListRemote(owner="seppeljordan", repo="pypi2nix"),
            lambda i: pypi2nix_list_remote,
        ),
        (
            nix_prefetch_github.CalculateSha256Sum(
                owner="seppeljordan",
                repo="pypi2nix",
                revision=pypi2nix_list_remote.branch("master"),
            ),
            lambda i: "TEST_ACTUALHASH",
        ),
    ]
    effect = nix_prefetch_github.prefetch_github(
        owner="seppeljordan", repo="pypi2nix", prefetch=False, rev="refs/heads/master"
    )
    prefetch_result = perform_sequence(sequence, effect)
    assert prefetch_result.rev == pypi2nix_list_remote.branch("master")
    assert prefetch_result.sha256 == "TEST_ACTUALHASH"


def test_that_prefetch_github_understands_fetch_submodules(pypi2nix_list_remote):
    sequence = [
        (
            nix_prefetch_github.GetListRemote(owner="seppeljordan", repo="pypi2nix"),
            lambda i: pypi2nix_list_remote,
        ),
        (
            nix_prefetch_github.CalculateSha256Sum(
                owner="seppeljordan",
                repo="pypi2nix",
                revision=pypi2nix_list_remote.branch("master"),
                fetch_submodules=True,
            ),
            lambda i: "TEST_ACTUALHASH",
        ),
    ]
    effect = nix_prefetch_github.prefetch_github(
        owner="seppeljordan", repo="pypi2nix", prefetch=False, fetch_submodules=True
    )
    perform_sequence(sequence, effect)
