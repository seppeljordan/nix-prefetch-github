{ mkShell, git, nixfmt, nix-prefetch-scripts, pandoc, python3 }:
mkShell {
  packages = [ git nixfmt nix-prefetch-scripts pandoc ] ++ (with python3.pkgs; [
    black
    flake8
    mypy
    twine
    virtualenv
    isort
    coverage
    pydeps
    pip
  ]);
  inputsFrom = [ python3.pkgs.nix-prefetch-github ];
}
