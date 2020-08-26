{
  description = "nix-prefetch-github";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    let
      f = import ./default.nix;
      systemDependent = flake-utils.lib.eachDefaultSystem (system:
        let pkgs = nixpkgs.outputs.legacyPackages."${system}";
        in { defaultPackage = pkgs.python3.pkgs.callPackage f { }; });
      overlay = final: prev: {
        nix-prefetch-github = final.python3.pkgs.callPackage f { };
      };
      systemIndependent = { inherit overlay; };
    in systemDependent // systemIndependent;
}
