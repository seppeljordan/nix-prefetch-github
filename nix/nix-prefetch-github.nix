{ buildPythonPackage, attrs, effect, git }:
buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "dev";
  src = ../.;
  propagatedBuildInputs = [ attrs effect ];
  checkInputs = [ git ];
  checkPhase = ''
    python -m unittest discover
  '';
  DISABLED_TESTS = "network requires_nix_build";
}
