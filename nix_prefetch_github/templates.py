_OUTPUT_TEMPLATE = """let
  pkgs = import <nixpkgs> {{}};
in
  pkgs.fetchFromGitHub {{
    owner = "{owner}";
    repo = "{repo}";
    rev = "{rev}";
    sha256 = "{sha256}";{fetch_submodules}{leave_dot_git}{deep_clone}
  }}
"""


def output_template(
    owner: str,
    repo: str,
    rev: str,
    sha256: str,
    fetch_submodules: bool,
    leave_dot_git: bool,
    deep_clone: bool,
) -> str:
    return _OUTPUT_TEMPLATE.format(
        owner=owner,
        repo=repo,
        rev=rev,
        sha256=sha256,
        fetch_submodules="\n    fetchSubmodules = true;" if fetch_submodules else "",
        leave_dot_git="\n    leaveDotGit = true;" if leave_dot_git else "",
        deep_clone="\n    deepClone = true;" if deep_clone else "",
    )
