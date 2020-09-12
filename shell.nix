{ nixpkgs ? import <nixpkgs> { } }:
let
  python = nixpkgs.python3.override {
    packageOverrides = import nix/package-overrides.nix;
  };
in python.pkgs.nix-prefetch-github
