{
  buildPythonPackage,
  git,
  which,
  sphinxHook,
  sphinx-argparse,
  pytestCheckHook,

  parameterized,
  setuptools,
}:
let
  version = builtins.readFile ../nix_prefetch_github/VERSION;
in
buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "${version}-dev";
  outputs = [
    "out"
    "doc"
    "man"
  ];
  src = ../.;
  pyproject = true;
  nativeBuildInputs = [
    sphinxHook
    sphinx-argparse
    setuptools
  ];
  nativeCheckInputs = [
    git
    which
    pytestCheckHook
  ];
  postInstall = ''
    for f in $out/bin/* ; do
        wrapProgram "$f" --suffix PATH : "${git}/bin"
    done
  '';
  checkInputs = [
    git
    which
    pytestCheckHook
    parameterized
  ];
  sphinxBuilders = [
    "singlehtml"
    "man"
  ];
  sphinxRoot = "docs";
  DISABLED_TESTS = "network requires_nix_build";
}
