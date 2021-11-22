from dataclasses import dataclass
from typing import Optional, Protocol

from .repository import GithubRepository

trash_sha256 = "1y4ly7lgqm03wap4mh01yzcmvryp29w739fy07zzvz15h2z9x3dv"


@dataclass
class PrefetchOptions:
    fetch_submodules: bool = False
    deep_clone: bool = False
    leave_dot_git: bool = False


class UrlHasher(Protocol):
    def calculate_sha256_sum(
        self,
        repository: GithubRepository,
        revision: str,
        prefetch_options: PrefetchOptions,
    ) -> Optional[str]:
        pass
