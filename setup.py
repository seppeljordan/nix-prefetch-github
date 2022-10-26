import os
import os.path
from typing import Any, Iterable

from mypyc.build import mypycify
from setuptools import setup

# Comilation with `mypyc` can be disabled by specifying
# 'USE_MYPYC=False' as an environment variable.
USE_MYPYC = not (os.getenv("USE_MYPYC", "True") == "False")


paths = [
    {
        "nix_prefetch_github": [
            "alerter.py",
            "dependency_injector.py",
            "functor.py",
            "github.py",
            "hash.py",
            "list_remote.py",
            "list_remote_factory.py",
            "logging.py",
            "prefetch.py",
            "process_environment.py",
            "repository_detector.py",
            "revision_index.py",
            "revision_index_factory.py",
            "run_tests.py",
            "templates.py",
            "views.py",
            {
                "url_hasher": [
                    "nix_build.py",
                    "nix_prefetch.py",
                    "url_hasher_selector.py",
                ],
                "command": [
                    "command_availability_checker.py",
                    "command_runner.py",
                ],
            },
        ]
    }
]


def files_to_compile(paths: Any) -> Iterable[str]:
    for path in paths:
        if isinstance(path, dict):
            for key, value in path.items():
                yield from (
                    os.path.join(key, subpath) for subpath in files_to_compile(value)
                )
        else:
            yield path


setup(
    ext_modules=mypycify(list(files_to_compile(paths))) if USE_MYPYC else [],
)
