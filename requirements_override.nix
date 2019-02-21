{ pkgs, python }:

let
  isPytest = drv: with builtins; with pkgs.lib;
    let
      name = (parseDrvName drv.name).name;
    in
      hasSuffix "pytest" name;
  applyTransformations = transformations: package:
    pkgs.lib.fold
    (transformation: pkg: pkg.overrideDerivation transformation)
    package
    transformations;
  addTestPhase = testPhaseContent: old: {
    installCheckPhase = testPhaseContent;
  };
  enableTests = old: {
    doInstallCheck = true;
  };
  addBuildInputs = inputs: old: {
    buildInputs = old.buildInputs ++ inputs;
  };
in

self: super:
let
  addDependencies = deps: old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++
    builtins.map
    (dependencyName: self."${dependencyName}")
    deps;
  };
in
{
  "attrs" = super.attrs.overrideDerivation (old: {
    propagatedBuildInputs = builtins.filter (x: ! isPytest x) old.propagatedBuildInputs;
  });
  "py" = super.py.overrideDerivation (old: {
    buildInputs = old.buildInputs ++ [self.setuptools-scm];
  });
  "twine" = super.twine.overrideDerivation(old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [self.readme-renderer];
  });
  "nix-prefetch-github" =
    applyTransformations
    [
      (addDependencies ["pytest" "pytest-cov" "twine"])
      (addTestPhase ''
        pytest tests/ -m 'not nix_build'
      ''
      )
      enableTests
      (addBuildInputs [pkgs.git])
    ]
    super."nix-prefetch-github";
}
