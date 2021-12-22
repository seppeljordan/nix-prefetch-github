{ buildPythonPackage, git }:
let version = builtins.readFile ../nix_prefetch_github/VERSION;
in buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "${version}-dev";
  src = ../.;
  checkInputs = [ git ];
  checkPhase = ''
    python -m unittest discover
  '';
  DISABLED_TESTS = "network requires_nix_build";
}
