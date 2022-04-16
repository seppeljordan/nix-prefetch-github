from unittest import TestCase

from nix_prefetch_github.list_remote import ListRemote
from nix_prefetch_github.revision_index import RevisionIndexImpl


class RevisionIndexTests(TestCase):
    def setUp(self) -> None:
        self.index = RevisionIndexImpl(self.remote_list)

    @property
    def remote_list(self) -> ListRemote:
        return ListRemote(
            heads={"test-branch-1": "1", "test-branch-2": "2", "master": "master-ref"},
            tags={
                "tag-1^{}": "tag-1-ref-annotated",
                "tag-1": "tag-1-ref",
                "tag-2": "tag-2-ref",
            },
            symrefs={"HEAD": "master"},
        )

    def test_revision_on_test_branch_1_is_1(self) -> None:
        expected_revision = "1"
        revision = self.index.get_revision_by_name("test-branch-1")
        self.assertEqual(revision, expected_revision)

    def test_revision_on_test_branch_2_is_2(self) -> None:
        expected_revision = "2"
        revision = self.index.get_revision_by_name("test-branch-2")
        self.assertEqual(revision, expected_revision)

    def test_revision_for_tag_1_is_tag_1_ref_annotated(self) -> None:
        revision = self.index.get_revision_by_name("tag-1")
        self.assertEqual(revision, "tag-1-ref-annotated")

    def test_revision_for_tag_2_is_tag_2_ref_annotated(self) -> None:
        revision = self.index.get_revision_by_name("tag-2")
        self.assertEqual(revision, "tag-2-ref")

    def test_head_ref_points_to_master_ref(self) -> None:
        revision = self.index.get_revision_by_name("HEAD")
        self.assertEqual(revision, "master-ref")

    def test_can_get_ref_for_refs_heads_master(self) -> None:
        revision = self.index.get_revision_by_name("refs/heads/master")
        self.assertEqual(revision, "master-ref")
