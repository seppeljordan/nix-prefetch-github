{ buildPythonApplication, attrs, effect, click, pytest, pytest-black, pytestcov
, pytest-isort, twine, black, mypy, nixfmt, jinja2, flake8 }:
buildPythonApplication {
  pname = "nix-prefetch-github";
  version = "dev";
  src = ./.;
  propagatedBuildInputs = [ attrs click effect jinja2 ];
  buildInputs = [ nixfmt ];
  checkInputs = [
    flake8
    jinja2
    pytest
    pytest-black
    pytestcov
    pytest-isort
    twine
    black
    mypy
  ];
  checkPhase = ''
    pytest -m 'not network'
  '';
}
