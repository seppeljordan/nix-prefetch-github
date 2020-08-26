{
  description = "nix-prefetch-github";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        f = import ./default.nix;
        pkgs = nixpkgs.outputs.legacyPackages."${system}";
      in {
        defaultPackage = pkgs.python3.pkgs.callPackage f { };
      });
}
