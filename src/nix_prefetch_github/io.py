import subprocess


def cmd(command):
    process_return = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    return process_return.returncode, process_return.stdout
