{ buildPythonPackage, git, which, sphinxHook, sphinx-argparse, mypy }:
let version = builtins.readFile ../nix_prefetch_github/VERSION;
in buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "${version}-dev";
  outputs = [ "out" "doc" "man" ];
  src = ../.;
  nativeBuildInputs = [ sphinxHook sphinx-argparse mypy ];
  checkInputs = [ git which ];
  checkPhase = ''
    python -m nix_prefetch_github.run_tests
  '';
  sphinxBuilders = [ "singlehtml" "man" ];
  sphinxRoot = "docs";
  DISABLED_TESTS = "network requires_nix_build";
}
