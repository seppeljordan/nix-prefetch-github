import pytest

from nix_prefetch_github.list_remote import ListRemote, RefKind


@pytest.fixture
def test_output():
    return """From git@github.com:seppeljordan/nix-prefetch-github.git
ref: refs/heads/master	HEAD
9ce3bcc3610ffeb36f53bc690682f48c8d311764	HEAD
9ce3bcc3610ffeb36f53bc690682f48c8d311764	refs/heads/master
c4e967f4a80e0c030364884e92f2c3cc39ae3ef2	refs/heads/travis-setup
1234567789473873487438239389538913598723	refs/heads/test/branch
c4e967f4a80e0c030364884e92f2c3cc39ae3ef2	refs/pull/1/head
c4f752b05270fd1ab812c4f6a41ddcd8769eb2e6	refs/pull/2/head
ac17b18f3ba68bcea84b563523dfe82729e49aa8	refs/pull/5/head
f7e74db312def6d0e57028b2b630962c768eeb9f	refs/pull/7/head
b12ab7fe187924d8536d27b2ddf3bcccd2612b32	refs/tags/1.3
cffdbcb3351f500b5ca8867a65261443b576b215	refs/tags/v2.0
0b63b78df5e5e17fa46cbdd8aac2b56e8622e5d3	refs/tags/v2.1
9ce3bcc3610ffeb36f53bc690682f48c8d311764	refs/tags/v2.2
"""


@pytest.fixture
def remote_list(test_output):
    return ListRemote.from_git_ls_remote_output(test_output)


def test_contains_master_branch(remote_list):
    assert remote_list.branch("master") == "9ce3bcc3610ffeb36f53bc690682f48c8d311764"


def test_branch_returns_none_for_unknown_branch(remote_list):
    assert remote_list.branch("does not exist") is None


def test_contains_HEAD_symref(remote_list):
    assert remote_list.symref("HEAD") == "master"


def test_symref_returns_none_for_unknown_reference_name(remote_list):
    assert remote_list.symref("unknown") is None


def test_contains_tag_v2_0(remote_list):
    assert remote_list.tag("v2.0") == "cffdbcb3351f500b5ca8867a65261443b576b215"


def test_tag_returns_none_for_unkown_tag(remote_list):
    assert remote_list.tag("unkown") is None


def test_branch_with_slash_is_recognized(remote_list):
    assert (
        remote_list.branch("test/branch") == "1234567789473873487438239389538913598723"
    )


def test_kind_from_ref_can_detect_tags():
    assert ListRemote.kind_from_ref("refs/tags/my_tag") == RefKind.Tag
