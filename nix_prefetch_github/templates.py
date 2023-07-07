_OUTPUT_TEMPLATE = """let
  pkgs = import <nixpkgs> {{}};
in
  pkgs.fetchFromGitHub {{
    owner = "{owner}";
    repo = "{repo}";
    rev = "{rev}";
    hash = "{hash_sum}";{fetch_submodules}{leave_dot_git}{deep_clone}
  }}
"""


def _render_line_if_enabled(line: str, condition: bool) -> str:
    return f"\n    {line};" if condition else ""


def output_template(
    owner: str,
    repo: str,
    rev: str,
    hash_sum: str,
    fetch_submodules: bool,
    leave_dot_git: bool,
    deep_clone: bool,
) -> str:
    return _OUTPUT_TEMPLATE.format(
        owner=owner,
        repo=repo,
        rev=rev,
        hash_sum=hash_sum,
        fetch_submodules=_render_line_if_enabled(
            "fetchSubmodules = true", fetch_submodules
        ),
        leave_dot_git=_render_line_if_enabled("leaveDotGit = true", leave_dot_git),
        deep_clone=_render_line_if_enabled("deepClone = true", deep_clone),
    )
