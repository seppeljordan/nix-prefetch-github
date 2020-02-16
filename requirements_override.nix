{ pkgs, python }:

self: super:

{
  "nix-prefetch-github" = super."nix-prefetch-github".overrideDerivation (old: {
    propagatedBuildInptus = with self;
      [ pytest pytest-cov twine black mypy flake8 ]
      ++ old.propagatedBuildInputs;
    doCheck = true;
    checkPhase = ''
      pytest tests/ -m 'not not_nix_build'
    '';
    buildInputs = old.buildInputs ++ [ pkgs.git ];
    shellHook = ''
      export PATH=$PWD/scripts:$PATH
      export PYTHONPATH=$PWD/src:$PYTHONPATH
    '';
  });

  "pytest-black" = super."pytest-black".overrideDerivation
    (old: { buildInputs = old.buildInputs ++ [ self."setuptools-scm" ]; });
}
