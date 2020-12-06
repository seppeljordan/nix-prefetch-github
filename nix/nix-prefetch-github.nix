{ buildPythonPackage, attrs, effect, click, pytest, pytestcov, isort, twine
, black, mypy, nixfmt, jinja2, flake8, git, pydeps, virtualenv, lib }:
let
  sourceFilter = with lib;
    with builtins;
    path: type:
    let
      filename = baseNameOf path;
      filters = [
        (type == "directory" && filename == ".git")
        (type == "regular" && hasSuffix "pyc" filename)
        (type == "regular" && hasSuffix "~" filename)
        (type == "directory" && filename == ".mypy_cache")
        (type == "directory" && filename == ".pytest_cache")
        (type == "directory" && filename == ".egg-info")
      ];
    in foldl (accu: elem: accu && (!elem)) true filters;
in buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "dev";
  src = builtins.path {
    path = ./..;
    filter = sourceFilter;
  };
  propagatedBuildInputs = [ attrs click effect jinja2 ];
  buildInputs = [ nixfmt pydeps ];
  checkInputs = [
    black
    flake8
    git
    jinja2
    mypy
    pydeps
    pytest
    pytestcov
    twine
    virtualenv
    isort
  ];
  checkPhase = ''
    pytest -m 'not network'
    $out/bin/nix-prefetch-github --help
    $out/bin/nix-prefetch-github-directory --help
    $out/bin/nix-prefetch-github-latest-release --help
  '';
}
