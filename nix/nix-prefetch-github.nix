{ buildPythonPackage, attrs, effect, pytestCheckHook, git }:
buildPythonPackage {
  pname = "nix-prefetch-github";
  version = "dev";
  src = ../.;
  propagatedBuildInputs = [ attrs effect ];
  disabledTests = [ "network" "requires_nix_build" ];
  checkInputs = [ git ];
  buildInputs = [ pytestCheckHook ];
}
