{ pkgs, python }:

let
  isPytest = drv: with builtins; with pkgs.lib;
    let
      name = (parseDrvName drv.name).name;
    in
      hasSuffix "pytest" name;
in

self: super:
let
  addDependencies = deps: packageName: super."${packageName}".overrideDerivation( old: {
    propagatedBuildInputs = old.propagatedBuildInputs ++
    builtins.map
    (dependencyName: builtins.trace dependencyName self."${dependencyName}")
    deps;
  });
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
    addDependencies
    ["pytest" "pytest-cov"]
    "nix-prefetch-github";
}
