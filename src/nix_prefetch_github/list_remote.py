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
                _, _, branch_name = ref.split("/")
                symrefs[suffix] = branch_name
            else:
                try:
                    _, kind, name = suffix.split("/")
                except ValueError:
                    continue
                if kind == "heads":
                    heads[name] = prefix
                elif kind == "tags":
                    tags[name] = prefix
        return constructor(heads=heads, symrefs=symrefs, tags=tags)

    def branch(self, branch_name):
        return self.heads.get(branch_name)

    def symref(self, ref_name):
        return self.symrefs.get(ref_name)

    def tag(self, tag_name):
        return self.tags.get(tag_name)
