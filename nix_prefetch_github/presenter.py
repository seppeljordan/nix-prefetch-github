import json

from .interfaces import PrefetchFailure, PrefetchOptions
from .prefetch import PrefetchedRepository
from .templates import output_template


def to_nix_expression(
    prefetched: PrefetchedRepository, options: PrefetchOptions
) -> str:
    return output_template(
        owner=prefetched.repository.owner,
        repo=prefetched.repository.name,
        rev=prefetched.rev,
        sha256=prefetched.sha256,
        fetch_submodules=options.fetch_submodules,
    )


def to_json_string(prefetched: PrefetchedRepository, options: PrefetchOptions) -> str:
    return json.dumps(
        {
            "owner": prefetched.repository.owner,
            "repo": prefetched.repository.name,
            "rev": prefetched.rev,
            "sha256": prefetched.sha256,
            "fetchSubmodules": options.fetch_submodules,
        },
        indent=4,
    )


def render_prefetch_failure(failure: PrefetchFailure) -> str:
    return "Prefetch failed: " + str(failure.reason)
