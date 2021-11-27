import os
import shlex
import subprocess
import sys
from typing import Dict, List, Optional, Tuple


def run_command(
    command: List[str],
    cwd: Optional[str] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    merge_stderr: bool = False,
) -> Tuple[int, str]:
    if environment_variables is None:
        environment_variables = dict()
    target_environment = dict(os.environ, **environment_variables)
    stderr = subprocess.STDOUT if merge_stderr else subprocess.PIPE
    print(f"Running command: {shlex.join(command)}", file=sys.stderr)
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
        print(process_stdout, file=sys.stderr)
    else:
        print(process_stderr, file=sys.stderr)
    return process.returncode, process_stdout
