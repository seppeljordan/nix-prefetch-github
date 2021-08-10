{ buildPythonPackage, attrs, effect, click, pytestCheckHook, git }:
buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "dev";
  src = ../.;
  propagatedBuildInputs = [ attrs click effect ];
  disabledTests = [ "network" "requires_nix_build" ];
  checkInputs = [ git ];
  buildInputs = [ pytestCheckHook ];
}
