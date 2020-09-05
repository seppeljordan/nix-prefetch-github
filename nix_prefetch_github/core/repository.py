from attr import attrib, attrs


@attrs
class GithubRepository:
    owner = attrib()
    name = attrib()

    def url(self):
        return f"https://github.com/{self.owner}/{self.name}.git"
