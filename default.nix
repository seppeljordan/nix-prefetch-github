{ nixpkgs ? import <nixpkgs> { } }:
let pkgs = (import ./requirements.nix { pkgs = nixpkgs; });

in pkgs.mkDerivation {
  pname = "nix-prefetch-github";
  version = "dev";
  src = ./.;
  propagatedBuildInputs = with pkgs.packages; [ attrs click effect jinja2 ];
  buildInputs = [ ];
  checkInputs = with pkgs.packages; [
    flake8
    jinja2
    pytest
    pytest-black
    pytest-cov
    pytest-isort
    twine
    readme-renderer
    black
    mypy
    nixpkgs.nixfmt
  ];
  shellHook = ''
    export PYTHONPATH=$PWD/src:$PYTHONPATH
  '';
}
