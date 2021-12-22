from dataclasses import dataclass


@dataclass(frozen=True)
class GithubRepository:
    owner: str
    name: str

    def url(self) -> str:
        return f"https://github.com/{self.owner}/{self.name}.git"
