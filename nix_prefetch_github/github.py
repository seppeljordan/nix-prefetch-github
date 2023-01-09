import json
from dataclasses import dataclass
from logging import Logger
from typing import Optional
from urllib.error import HTTPError
from urllib.request import urlopen

from nix_prefetch_github.interfaces import GithubRepository


@dataclass
class GithubAPIImpl:
    logger: Logger

    def get_tag_of_latest_release(self, repository: GithubRepository) -> Optional[str]:
        url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/releases/latest"
        try:
            with urlopen(url) as response:
                encoding = response.info().get_content_charset("utf-8")
                content_data = response.read()
        except HTTPError as e:
            self.logger.error(e)
            return None
        content_json = json.loads(content_data.decode(encoding))
        return content_json.get("tag_name")
