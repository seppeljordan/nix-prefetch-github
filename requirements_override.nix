{ pkgs, python }:

self: super:

{
  "pytest-black" = super."pytest-black".overrideDerivation
    (old: { buildInputs = old.buildInputs ++ [ self."setuptools-scm" ]; });
}
