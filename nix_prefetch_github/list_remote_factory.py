from dataclasses import dataclass
from typing import Optional

from .command import run_command
from .list_remote import ListRemote
from .repository import GithubRepository


@dataclass(frozen=True)
class ListRemoteFactoryImpl:
    def get_list_remote(self, repository: GithubRepository) -> Optional[ListRemote]:
        repository_url = repository.url()
        returncode, output = run_command(
            command=["git", "ls-remote", "--symref", repository_url],
            environment_variables={"GIT_ASKPASS": "", "GIT_TERMINAL_PROMPT": "0"},
            merge_stderr=False,
        )
        if returncode == 0:
            return ListRemote.from_git_ls_remote_output(output)
        else:
            return None
