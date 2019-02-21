import os
from tempfile import TemporaryDirectory

import nix_prefetch_github
import pytest
from effect import Effect, sync_perform
from effect.testing import perform_sequence
from nix_prefetch_github.io import cmd


requires_nix_build = pytest.mark.nix_build


def test_prefetch_github_actual_prefetch():
    seq = [
        (
            nix_prefetch_github.GetCommitHashForName(
                owner='seppeljordan',
                repo='pypi2nix',
                rev=None,
            ),
            lambda i: 'TEST_COMMIT',
        ),
        (
            nix_prefetch_github.TryPrefetch(
                owner='seppeljordan',
                repo='pypi2nix',
                rev='TEST_COMMIT',
                sha256=nix_prefetch_github.trash_sha256,
            ),
            lambda i: {
                'output':
                "output path TESTPATH has TEST hash 'TEST_ACTUALHASH' when TESTREST"
            }
        ),
        (
            nix_prefetch_github.TryPrefetch(
                owner='seppeljordan',
                repo='pypi2nix',
                rev='TEST_COMMIT',
                sha256='TEST_ACTUALHASH',
            ),
            lambda i: None
        )
    ]
    eff = nix_prefetch_github.prefetch_github(
        owner='seppeljordan',
        repo='pypi2nix',
        prefetch=True
    )
    prefetch_result = perform_sequence(seq, eff)
    assert prefetch_result['rev'] == 'TEST_COMMIT'
    assert prefetch_result['sha256'] == 'TEST_ACTUALHASH'


def test_prefetch_github_no_actual_prefetch():
    seq = [
        (
            nix_prefetch_github.GetCommitHashForName(
                owner='seppeljordan',
                repo='pypi2nix',
                rev=None,
            ),
            lambda i: 'TEST_COMMIT',
        ),
        (
            nix_prefetch_github.TryPrefetch(
                owner='seppeljordan',
                repo='pypi2nix',
                rev='TEST_COMMIT',
                sha256=nix_prefetch_github.trash_sha256,
            ),
            lambda i: {
                'output':
                "output path TESTPATH has TEST hash 'TEST_ACTUALHASH' when TESTREST"
            }
        ),
    ]
    eff = nix_prefetch_github.prefetch_github(
        owner='seppeljordan',
        repo='pypi2nix',
        prefetch=False,
    )
    prefetch_result = perform_sequence(seq, eff)
    assert prefetch_result['rev'] == 'TEST_COMMIT'
    assert prefetch_result['sha256'] == 'TEST_ACTUALHASH'


def test_prefetch_github_rev_given():
    commit_hash = '50553a665d2700c353ac41ab28c23b1027b7c1f0'
    seq = [
        (
            nix_prefetch_github.TryPrefetch(
                owner='seppeljordan',
                repo='pypi2nix',
                rev=commit_hash,
                sha256=nix_prefetch_github.trash_sha256
            ),
            lambda i: {
                'output':
                "garbage_output\noutput path TESTPATH has TEST hash 'TEST_ACTUALHASH' when TESTREST"
            }
        )
    ]
    eff = nix_prefetch_github.prefetch_github(
        owner='seppeljordan',
        repo='pypi2nix',
        prefetch=False,
        rev=commit_hash,
    )
    prefetch_result = perform_sequence(seq, eff)
    assert prefetch_result['rev'] == commit_hash
    assert prefetch_result['sha256'] == 'TEST_ACTUALHASH'


@requires_nix_build
def test_life_mode():
    results = nix_prefetch_github.nix_prefetch_github(
        owner='seppeljordan',
        repo='pypi2nix',
        prefetch=True,
        rev=None
    )
    assert 'sha256' in results.keys()


@requires_nix_build
def test_get_commit_hash_for_name_with_actual_github_repo():
    result = sync_perform(
        nix_prefetch_github.dispatcher(),
        Effect(nix_prefetch_github.GetCommitHashForName(
            owner='seppeljordan',
            repo='parsemon2',
            rev='master',
        ))
    )
    assert len(result) == 40


def test_is_sha1_hash_detects_actual_hash():
    text = '5a484700f1006389847683a72cd88bf7057fe772'
    assert nix_prefetch_github.is_sha1_hash(text)


def test_is_sha1_hash_returns_false_for_string_to_short():
    text = '5a484700f1006389847683a72cd88bf7057fe77'
    assert len(text) < 40
    assert not nix_prefetch_github.is_sha1_hash(text)


@requires_nix_build
def test_is_to_nix_expression_outputs_valid_nix_expr():
    for prefetch in [False, True]:
        output_dictionary = nix_prefetch_github.nix_prefetch_github(
            owner='seppeljordan',
            repo='pypi2nix',
            prefetch=prefetch,
            rev='master'
        )
        nix_expr_output = nix_prefetch_github.to_nix_expression(output_dictionary)

        with TemporaryDirectory() as temp_dir_name:
            nix_filename = temp_dir_name + '/output.nix'
            with open(nix_filename, 'w') as f:
                f.write(nix_expr_output)
            returncode, output = cmd(['nix-build', nix_filename, '--no-out-link'])
            assert returncode == 0
