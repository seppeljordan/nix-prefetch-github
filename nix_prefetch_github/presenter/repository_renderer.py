import json

from nix_prefetch_github.interfaces import PrefetchedRepository
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
