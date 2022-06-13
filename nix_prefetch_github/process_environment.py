import os


class ProcessEnvironmentImpl:
    def get_cwd(self) -> str:
        return os.getcwd()
