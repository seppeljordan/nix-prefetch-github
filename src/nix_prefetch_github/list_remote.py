from enum import Enum, unique


@unique
class RefKind(Enum):
    Head = 1
    Tag = 2


class ListRemote:
    def __init__(self, symrefs=dict(), heads=dict(), tags=dict()):
        self.heads = heads
        self.symrefs = symrefs
        self.tags = tags

    @classmethod
    def from_git_ls_remote_output(constructor, output):
        symrefs = dict()
        heads = dict()
        tags = dict()
        for line in output.splitlines():
            try:
                prefix, suffix = line.split("\t")
            except ValueError:
                continue
            if line.startswith("ref: "):
                ref = prefix[5:]
                branch_name = constructor.name_from_ref(ref)
                symrefs[suffix] = branch_name
            else:
                try:
                    kind = constructor.kind_from_ref(suffix)
                except ValueError:
                    continue
                name = constructor.name_from_ref(suffix)
                if kind == RefKind.Head:
                    heads[name] = prefix
                elif kind == RefKind.Tag:
                    tags[name] = prefix
        return constructor(heads=heads, symrefs=symrefs, tags=tags)

    def branch(self, branch_name):
        return self.heads.get(branch_name)

    def symref(self, ref_name):
        return self.symrefs.get(ref_name)

    def tag(self, tag_name):
        return self.tags.get(tag_name)

    @classmethod
    def name_from_ref(constructor, ref):
        fragments = ref.split("/")
        # the first two fragments are exprected to be "refs" and
        # "heads", after that the proper ref name should appear
        return "/".join(fragments[2:])

    @classmethod
    def kind_from_ref(constructor, ref: str) -> RefKind:
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
