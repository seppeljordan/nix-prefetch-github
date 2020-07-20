import subprocess


def cmd(command, merge_stderr=True):
    stderr = subprocess.STDOUT if merge_stderr else subprocess.PIPE
    process_return = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=stderr, universal_newlines=True
    )
    return process_return.returncode, process_return.stdout
