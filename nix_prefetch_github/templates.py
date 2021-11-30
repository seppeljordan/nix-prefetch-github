_OUTPUT_TEMPLATE = """let
  pkgs = import <nixpkgs> {{}};
in
  pkgs.fetchFromGitHub {{
    owner = "{owner}";
    repo = "{repo}";
    rev = "{rev}";
    sha256 = "{sha256}";{fetch_submodules}
  }}
"""


def output_template(
    owner: str, repo: str, rev: str, sha256: str, fetch_submodules: bool
) -> str:
    return _OUTPUT_TEMPLATE.format(
        owner=owner,
        repo=repo,
        rev=rev,
        sha256=sha256,
        fetch_submodules="\n    fetchSubmodules = true;" if fetch_submodules else "",
    )
