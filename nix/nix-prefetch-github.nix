{ buildPythonPackage, git, which, sphinxHook, sphinx-argparse, pytestCheckHook

, parameterized }:
let version = builtins.readFile ../nix_prefetch_github/VERSION;
in buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "${version}-dev";
  outputs = [ "out" "doc" "man" ];
  src = ../.;
  nativeBuildInputs = [ sphinxHook sphinx-argparse ];
  nativeCheckInputs = [ git which pytestCheckHook ];
  postInstall = ''
    for f in $out/bin/* ; do
        wrapProgram "$f" --suffix PATH : "${git}/bin"
    done
  '';
  checkInputs = [ git which pytestCheckHook parameterized ];
  sphinxBuilders = [ "singlehtml" "man" ];
  sphinxRoot = "docs";
  DISABLED_TESTS = "network requires_nix_build";
}
