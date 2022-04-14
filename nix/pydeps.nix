{ buildPythonPackage, fetchPypi, stdlib-list }:
let
  pname = "pydeps";
  version = "1.10.14";
in buildPythonPackage {
  inherit pname version;
  src = fetchPypi {
    inherit pname version;
    sha256 = "ny5ZLENAA2gUdJeNhp9db5vO6z41Of41J+yOZnD34Ow=";
  };
  propagatedBuildInputs = [ stdlib-list ];
  doCheck = false;
}
