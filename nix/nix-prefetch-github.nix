{ buildPythonPackage, attrs, effect, click, pytest, pytest-black, pytestcov
, pytest-isort, twine, black, mypy, nixfmt, jinja2, flake8, git, pydeps, virtualenv }:
buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "dev";
  src = ./..;
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
    pytest-black
    pytest-isort
    pytestcov
    twine
    virtualenv
  ];
  checkPhase = ''
    flake8
    mypy
    pytest -m 'not network'
    $out/bin/nix-prefetch-github --help
    $out/bin/nix-prefetch-github-directory --help
    $out/bin/nix-prefetch-github-latest-release --help
  '';
}
