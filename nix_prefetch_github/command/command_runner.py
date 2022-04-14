import os
import shlex
import subprocess
from dataclasses import dataclass
from logging import Logger
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class CommandRunnerImpl:
    logger: Logger

    def run_command(
        self,
        command: List[str],
        cwd: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        merge_stderr: bool = False,
    ) -> Tuple[int, str]:
        if environment_variables is None:
            environment_variables = dict()
        target_environment = dict(os.environ, **environment_variables)
        stderr = subprocess.STDOUT if merge_stderr else subprocess.PIPE
        self.logger.info("Running command: %s", shlex.join(command))
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=stderr,
            universal_newlines=True,
            cwd=cwd,
            env=target_environment,
        )
        process_stdout, process_stderr = process.communicate()
        if merge_stderr:
            self.logger.info(process_stdout)
        else:
            self.logger.info(process_stderr)
        return process.returncode, process_stdout
