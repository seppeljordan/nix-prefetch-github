#!/usr/bin/env python

import json
import shlex
import shutil
import subprocess
import tempfile
import unittest
from os import path
from pathlib import Path
from typing import List, Optional

from nix_prefetch_github.tests import network, requires_nix_build


class TestCase(unittest.TestCase):
    def assertReturncode(
        self, command: List[str], expected_code: int, message: Optional[str] = None
    ) -> None:
        finished_process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        self.assertEqual(
            finished_process.returncode,
            expected_code,
            msg=self._prepare_failed_command_message(
                command=command,
                expected_code=expected_code,
                process=finished_process,
                msg=message,
            ),
        )

    def _prepare_failed_command_message(
        self,
        command: List[str],
        expected_code: int,
        process: subprocess.CompletedProcess,
        msg: Optional[str],
    ) -> str:
        result = f"Expected return code {expected_code} when running {command}, but got {process.returncode}"
        if msg is not None:
            result += ", " + msg
        result += f"\nstdout: {process.stdout}"
        result += f"\nstderr: {process.stderr}"
        return result


@network
@requires_nix_build
class FlakeCheckTest(TestCase):
    def test_that_flake_check_runs_successfully(self) -> None:
        self.assertReturncode(["nix", "flake", "check", "--print-build-logs"], 0)


@network
@requires_nix_build
class VersionFlagTests(TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.mkdtemp()
        self.output = path.join(self.directory, "result")
        subprocess.run(["nix", "build", "--out-link", self.output], capture_output=True)

    def test_can_specify_version_flag(self) -> None:
        commands = [
            "nix-prefetch-github",
            "nix-prefetch-github-directory",
            "nix-prefetch-github-latest-release",
        ]
        for command in commands:
            with self.subTest(msg=command):
                self.assertReturncode([f"{self.output}/bin/{command}", "--version"], 0)

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)


@network
@requires_nix_build
class NixEvaluationTests(TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.mkdtemp()
        self.output = path.join(self.directory, "result")
        subprocess.run(["nix", "build", "--out-link", self.output], capture_output=True)

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
        ]
        for expression in expressions:
            with self.subTest(msg=shlex.join(expression)):
                finished_process = subprocess.run(
                    expression, capture_output=True, universal_newlines=True
                )
                self.assertEqual(finished_process.returncode, 0)
                self.assertReturncode(
                    ["nix-build", "-E", finished_process.stdout, "--no-out-link"], 0
                )

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)


@network
@requires_nix_build
class JsonIntegrityTests(TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.mkdtemp()
        self.output = path.join(self.directory, "result")
        subprocess.run(["nix", "build", "--out-link", self.output], capture_output=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.directory)

    def test_can_load_json_output_as_json(self) -> None:
        expressions = [
            [
                f"{self.output}/bin/nix-prefetch-github",
                "seppeljordan",
                "nix-prefetch-github",
                "-v",
            ],
            [
                f"{self.output}/bin/nix-prefetch-github-latest-release",
                "seppeljordan",
                "nix-prefetch-github",
                "-v",
            ],
            [
                f"{self.output}/bin/nix-prefetch-github-directory",
                "-v",
            ],
        ]
        for expression in expressions:
            expression_shell_command = shlex.join(expression)
            with self.subTest(msg=expression_shell_command):
                finished_process = subprocess.run(
                    expression, capture_output=True, universal_newlines=True
                )
                self.assertEqual(
                    finished_process.returncode,
                    0,
                    msg="\n".join(
                        [
                            f"Failed to execute {expression_shell_command}.",
                            f"stdout: {finished_process.stdout}",
                            f"stderr: {finished_process.stderr}",
                        ]
                    ),
                )
                json.loads(finished_process.stdout)

    def test_can_use_json_output_as_input_for_fetch_from_github(self) -> None:
        expression = [
            f"{self.output}/bin/nix-prefetch-github",
            "seppeljordan",
            "nix-prefetch-github",
        ]
        finished_process = subprocess.run(
            expression, capture_output=True, check=True, universal_newlines=True
        )
        with open(Path(self.directory) / "output.json", "w") as handle:
            handle.write(finished_process.stdout)
        subprocess.run(
            [
                "nix",
                "build",
                "--impure",
                "--expr",
                "with import <nixpkgs> {}; with builtins; fetchFromGitHub (fromJSON (readFile ./output.json))",
            ],
            check=True,
            cwd=self.directory,
        )


if __name__ == "__main__":
    unittest.main()
