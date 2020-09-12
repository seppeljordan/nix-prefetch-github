{ buildPythonPackage, fetchPypi }:
buildPythonPackage rec {
  pname = "stdlib-list";
  version = "0.7.0";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-ZsHBckoSZnzbNb6fQxgcPmZGwZTmMe+qqTwfLCx6H38=";
  };
  doCheck = false;
}
