import json
from dataclasses import dataclass
from typing import Optional

from nix_prefetch_github.interfaces import (
    PrefetchedRepository,
    RenderingFormat,
    RepositoryRenderer,
)
from nix_prefetch_github.templates import output_template


class NixRepositoryRenderer:
    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        return output_template(
            owner=repository.repository.owner,
            repo=repository.repository.name,
            rev=repository.rev,
            sha256=repository.sha256,
            fetch_submodules=repository.options.fetch_submodules,
            leave_dot_git=repository.options.leave_dot_git,
            deep_clone=repository.options.deep_clone,
        )


class JsonRepositoryRenderer:
    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        return json.dumps(
            {
                "owner": repository.repository.owner,
                "repo": repository.repository.name,
                "rev": repository.rev,
                "sha256": repository.sha256,
                "fetchSubmodules": repository.options.fetch_submodules,
                "leaveDotGit": repository.options.leave_dot_git,
                "deepClone": repository.options.deep_clone,
            },
            indent=4,
        )


@dataclass
class RenderingSelectorImpl:
    nix_renderer: RepositoryRenderer
    json_renderer: RepositoryRenderer
    selected_output_format: Optional[RenderingFormat] = None

    def set_rendering_format(self, rendering_format: RenderingFormat) -> None:
        self.selected_output_format = rendering_format

    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        if self.selected_output_format == RenderingFormat.nix:
            return self.nix_renderer.render_prefetched_repository(repository)
        else:
            return self.json_renderer.render_prefetched_repository(repository)
