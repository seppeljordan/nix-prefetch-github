{ nixpkgs ? import <nixpkgs> { } }:
let f = import ./default.nix;

in nixpkgs.python3Packages.callPackage f { }
