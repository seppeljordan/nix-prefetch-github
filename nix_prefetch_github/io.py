import os
import subprocess
from copy import copy


def cmd(command, merge_stderr=True, cwd=None, environment_variables={}):
    current_environment = copy(os.environ)
    target_environment = dict(current_environment, **environment_variables)
    stderr = subprocess.STDOUT if merge_stderr else subprocess.PIPE
    process_return = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=stderr,
        universal_newlines=True,
        cwd=cwd,
        env=target_environment,
    )
    return process_return.returncode, process_return.stdout
