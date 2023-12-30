import io
import json
from dataclasses import dataclass
from datetime import datetime
from http.client import HTTPResponse
from json.decoder import JSONDecodeError
from logging import Logger
from typing import Any, Optional
from urllib.error import HTTPError
from urllib.request import urlopen

from nix_prefetch_github.interfaces import GithubRepository


@dataclass
class GithubAPIImpl:
    logger: Logger

    def get_tag_of_latest_release(self, repository: GithubRepository) -> Optional[str]:
        url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/releases/latest"
        self.logger.debug("Query github api @ %s", url)
        try:
            with urlopen(url) as response:
                response_json = self._decode_json_from_response(response)
        except (HTTPError, JSONDecodeError) as e:
            self.logger.error(e)
            return None
        return response_json.get("tag_name")

    def get_commit_date(
        self, repository: GithubRepository, commit_sha1_hash: str
    ) -> Optional[datetime]:
        url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/commits/{commit_sha1_hash}"
        self.logger.debug("Query github api @ %s", url)
        try:
            with urlopen(url) as response:
                response_json = self._decode_json_from_response(response)
        except (HTTPError, JSONDecodeError) as e:
            self.logger.error(e)
            return None
        date_string = response_json.get("commit", {}).get("committer", {}).get("date")
        try:
            return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError as e:
            self.logger.exception(e)
            return None

    def _decode_json_from_response(self, response: HTTPResponse) -> Any:
        return json.load(
            io.TextIOWrapper(
                response, encoding=response.info().get_content_charset("utf-8")
            )
        )
