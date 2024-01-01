import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from nix_prefetch_github.interfaces import (
    GithubAPI,
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
            hash_sum=repository.hash_sum,
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

    def render_to_json(self, repository: PrefetchedRepository) -> Dict[str, Any]:
        output: Dict[str, Any] = {
            "owner": repository.repository.owner,
            "repo": repository.repository.name,
            "rev": repository.rev,
            "hash": repository.hash_sum,
        }
        if repository.options.deep_clone != self.DEFAULTS["deepClone"]:
            output["deepClone"] = repository.options.deep_clone
        if repository.options.fetch_submodules != self.DEFAULTS["fetchSubmodules"]:
            output["fetchSubmodules"] = repository.options.fetch_submodules
        if repository.options.leave_dot_git != self.DEFAULTS["leaveDotGit"]:
            output["leaveDotGit"] = repository.options.leave_dot_git
        return output

    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        return json.dumps(
            self.render_to_json(repository),
            indent=4,
        )


@dataclass
class MetaRepositoryRenderer:
    json_renderer: JsonRepositoryRenderer
    github_api: GithubAPI

    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        src_output = self.json_renderer.render_to_json(repository)
        meta_output: Dict[str, Any] = dict()
        commit_timestamp = self.github_api.get_commit_date(
            repository.repository, repository.rev
        )
        if commit_timestamp:
            meta_output["commitDate"] = commit_timestamp.date().isoformat()
            meta_output["commitTimeOfDay"] = commit_timestamp.time().isoformat()
        return json.dumps(
            {
                "src": src_output,
                "meta": meta_output,
            },
            indent=4,
        )


@dataclass
class RenderingSelectorImpl:
    nix_renderer: RepositoryRenderer
    json_renderer: RepositoryRenderer
    meta_renderer: RepositoryRenderer
    selected_output_format: Optional[RenderingFormat] = None

    def set_rendering_format(self, rendering_format: RenderingFormat) -> None:
        self.selected_output_format = rendering_format

    def render_prefetched_repository(self, repository: PrefetchedRepository) -> str:
        if self.selected_output_format == RenderingFormat.nix:
            return self.nix_renderer.render_prefetched_repository(repository)
        elif self.selected_output_format == RenderingFormat.meta:
            return self.meta_renderer.render_prefetched_repository(repository)
        else:
            return self.json_renderer.render_prefetched_repository(repository)
