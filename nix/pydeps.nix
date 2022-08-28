{ buildPythonPackage, fetchPypi, stdlib-list }:
let
  pname = "pydeps";
  version = "1.10.22";
in buildPythonPackage {
  inherit pname version;
  src = fetchPypi {
    inherit pname version;
    sha256 = "2elvE6b7GFipYEEL95kzNuu6L31iMY0AynfU7stBW4o=";
  };
  propagatedBuildInputs = [ stdlib-list ];
  doCheck = false;
}
