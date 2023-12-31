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
        self.logger.info(
            f"Query latest release for repository {repository.owner}/{repository.name} from GitHub."
        )
        url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/releases/latest"
        response_json = self._request_json_document(url)
        if response_json is None:
            return None
        return response_json.get("tag_name")

    def get_commit_date(
        self, repository: GithubRepository, commit_sha1_hash: str
    ) -> Optional[datetime]:
        url = f"https://api.github.com/repos/{repository.owner}/{repository.name}/commits/{commit_sha1_hash}"
        response_json = self._request_json_document(url)
        if response_json is None:
            return None
        date_string = response_json.get("commit", {}).get("committer", {}).get("date")
        return self._parse_timestamp(date_string)

    def _parse_timestamp(self, timestamp: str) -> Optional[datetime]:
        try:
            return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError as e:
            self.logger.exception(e)
            return None

    def _request_json_document(self, url: str) -> Optional[Any]:
        self.logger.debug("GET JSON document from %s", url)
        try:
            with urlopen(url) as response:
                self.logger.debug(
                    "Response was %(status)s %(reason)s",
                    dict(status=response.status, reason=response.reason),
                )
                return self._decode_json_from_response(response)
        except (HTTPError, JSONDecodeError) as e:
            self.logger.error(e)
            return None

    def _decode_json_from_response(self, response: HTTPResponse) -> Any:
        return json.load(
            io.TextIOWrapper(
                response, encoding=response.info().get_content_charset("utf-8")
            )
        )
