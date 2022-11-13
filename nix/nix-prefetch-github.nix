{ buildPythonPackage, git, which, sphinxHook, sphinx-argparse, pytestCheckHook
}:
let version = builtins.readFile ../nix_prefetch_github/VERSION;
in buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "${version}-dev";
  outputs = [ "out" "doc" "man" ];
  src = ../.;
  nativeBuildInputs = [ sphinxHook sphinx-argparse ];
  checkInputs = [ git which pytestCheckHook ];
  sphinxBuilders = [ "singlehtml" "man" ];
  sphinxRoot = "docs";
  DISABLED_TESTS = "network requires_nix_build";
}
