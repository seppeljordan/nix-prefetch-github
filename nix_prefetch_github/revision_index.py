from dataclasses import dataclass
from typing import Optional

from nix_prefetch_github.list_remote import ListRemote


@dataclass(frozen=True)
class RevisionIndexImpl:
    remote_list: ListRemote

    def get_revision_by_name(self, name: str) -> Optional[str]:
        if self.remote_list is None:
            return None
        if (symref := self.remote_list.symref(name)) is not None:
            name = symref
        return (
            self.remote_list.full_ref_name(name)
            or self.remote_list.branch(name)
            or self.remote_list.tag(f"{name}^{{}}")
            or self.remote_list.tag(name)
        )
