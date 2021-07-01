{ buildPythonPackage, attrs, effect, click, pytest, pytestcov, isort, twine
, black, mypy, nixfmt, flake8, git, pydeps, virtualenv, lib }:
buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "dev";
  src = ../.;
  propagatedBuildInputs = [ attrs click effect ];
  buildInputs = [ nixfmt pydeps ];
  checkInputs =
    [ black flake8 git mypy pydeps pytest pytestcov twine virtualenv isort ];
  checkPhase = ''
    pytest -m 'not network and not requires_nix_build'
    $out/bin/nix-prefetch-github --help
    $out/bin/nix-prefetch-github-directory --help
    $out/bin/nix-prefetch-github-latest-release --help
  '';
}
