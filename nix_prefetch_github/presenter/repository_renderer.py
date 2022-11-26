import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

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
    DEFAULTS = {
        "fetchSubmodules": False,
        "leaveDotGit": False,
        "deepClone": False,
    }

    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        output: Dict[str, Any] = {
            "owner": repository.repository.owner,
            "repo": repository.repository.name,
            "rev": repository.rev,
            "sha256": repository.sha256,
        }
        if repository.options.deep_clone != self.DEFAULTS["deepClone"]:
            output["deepClone"] = repository.options.deep_clone
        if repository.options.fetch_submodules != self.DEFAULTS["fetchSubmodules"]:
            output["fetchSubmodules"] = repository.options.fetch_submodules
        if repository.options.leave_dot_git != self.DEFAULTS["leaveDotGit"]:
            output["leaveDotGit"] = repository.options.leave_dot_git
        return json.dumps(
            output,
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
