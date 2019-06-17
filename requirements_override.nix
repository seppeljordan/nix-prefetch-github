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
  addBuildDependencies = deps: old: {
    buildInputs = old.buildInputs ++
    builtins.map
    (dependencyName: self."${dependencyName}")
    deps;
  };
  addRuntimeDependencies = deps: old: {
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
  "py" = applyTransformations
    [
      (addBuildDependencies [ "setuptools-scm" ])
    ]
    super."py";
  "twine" = super.twine.overrideDerivation(old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++ [self.readme-renderer];
  });
  "nix-prefetch-github" =
    applyTransformations
    [
      (addBuildDependencies [
        "pytest"
        "pytest-cov"
        "twine"
      ])
      (addTestPhase ''
        python -m pytest tests/ -m 'not nix_build'
      ''
      )
      enableTests
      (addBuildInputs [pkgs.git])
    ]
    super."nix-prefetch-github";
}
