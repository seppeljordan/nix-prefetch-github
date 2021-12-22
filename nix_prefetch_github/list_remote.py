from __future__ import annotations

from enum import Enum, unique
from typing import Dict, Optional


@unique
class RefKind(Enum):
    Head = 1
    Tag = 2


class ListRemote:
    def __init__(
        self,
        symrefs: Dict[str, str] = dict(),
        heads: Dict[str, str] = dict(),
        tags: Dict[str, str] = dict(),
    ) -> None:
        self.heads = heads
        self.symrefs = symrefs
        self.tags = tags

    @classmethod
    def from_git_ls_remote_output(constructor, output: str) -> ListRemote:
        builder = _Builder()
        for line in output.splitlines():
            builder.parse_line(line)
        return builder.to_list_remote()

    def branch(self, branch_name: str) -> Optional[str]:
        return self.heads.get(branch_name)

    def symref(self, ref_name: str) -> Optional[str]:
        return self.symrefs.get(ref_name)

    def tag(self, tag_name: str) -> Optional[str]:
        return self.tags.get(tag_name)

    def full_ref_name(self, ref_name: str) -> Optional[str]:
        try:
            kind = kind_from_ref(ref_name)
        except ValueError:
            return None
        name = name_from_ref(ref_name)
        if not name:
            return None
        if kind == RefKind.Tag:
            return self.tag(name)
        elif kind == RefKind.Head:
            return self.branch(name)
        else:
            return None


class _Builder:
    def __init__(self) -> None:
        self.symrefs: Dict[str, str] = dict()
        self.heads: Dict[str, str] = dict()
        self.tags: Dict[str, str] = dict()

    def parse_line(self, line: str) -> None:
        try:
            prefix, suffix = line.split("\t")
        except ValueError:
            return
        if line.startswith("ref: "):
            ref = prefix[5:]
            branch_name = name_from_ref(ref)
            if branch_name:
                self.symrefs[suffix] = branch_name
        else:
            try:
                kind = kind_from_ref(suffix)
            except ValueError:
                return
            name = name_from_ref(suffix)
            if name:
                if kind == RefKind.Head:
                    self.heads[name] = prefix
                elif kind == RefKind.Tag:
                    self.tags[name] = prefix

    def to_list_remote(self) -> ListRemote:
        return ListRemote(symrefs=self.symrefs, heads=self.heads, tags=self.tags)


def name_from_ref(ref: str) -> Optional[str]:
    fragments = ref.split("/")
    # the first two fragments are exprected to be "refs" and
    # "heads", after that the proper ref name should appear
    return "/".join(fragments[2:]) or None


def kind_from_ref(ref: str) -> RefKind:
    fragments = ref.split("/")
    try:
        kind = fragments[1]
    except IndexError:
        raise ValueError(
            f"`{ref}` does not look like a proper entry from `git ls-remote`"
        )
    if kind == "heads":
        return RefKind.Head
    elif kind == "tags":
        return RefKind.Tag
    else:
        raise ValueError(f"Ref kind not recognized: `{kind}`")
