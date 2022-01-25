#!/usr/bin/env python

import shlex
import shutil
import subprocess
import tempfile
from os import path
from unittest import TestCase, main

from nix_prefetch_github.tests import network, requires_nix_build


@network
@requires_nix_build
class FlakeCheckTest(TestCase):
    def test_that_flake_check_runs_successfully(self) -> None:
        finished_process = subprocess.run(
            ["nix", "flake", "check", "--print-build-logs"]
        )
        self.assertEqual(finished_process.returncode, 0)


@network
@requires_nix_build
class NixEvaluationTests(TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.mkdtemp()
        self.output = path.join(self.directory, "result")
        subprocess.run(["nix", "build", "--out-link", self.output])

    def test_can_build_nix_expressions(self) -> None:
        expressions = [
            [
                f"{self.output}/bin/nix-prefetch-github",
                "seppeljordan",
                "nix-prefetch-github",
                "--nix",
                "-v",
            ],
            [
                f"{self.output}/bin/nix-prefetch-github-latest-release",
                "seppeljordan",
                "nix-prefetch-github",
                "--nix",
                "-v",
            ],
            [
                f"{self.output}/bin/nix-prefetch-github",
                "seppeljordan",
                "nix-prefetch-github",
                "--nix",
                "--leave-dot-git",
                "-v",
            ],
        ]
        for expression in expressions:
            with self.subTest(msg=shlex.join(expression)):
                finished_process = subprocess.run(expression, capture_output=True)
                self.assertEqual(finished_process.returncode, 0)
                build_process = subprocess.run(
                    ["nix-build", "-E", finished_process.stdout, "--no-out-link"]
                )
                self.assertEqual(build_process.returncode, 0)

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)


if __name__ == "__main__":
    main()
