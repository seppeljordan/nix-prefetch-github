{ buildPythonPackage, stdlib-list, fetchPypi }:
buildPythonPackage rec {
  pname = "pydeps";
  version = "1.9.9";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-3OuXIWfbnLpO5ib2h4Pzwl0T6QOu8Oqg7ieMhW77Yc0=";
  };
  propagatedBuildInputs = [ stdlib-list ];
  doCheck = false;
}
