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
        in {
          defaultPackage = with pkgs.python3.pkgs;
            toPythonApplication (callPackage f { });
        });
      overlay = final: prev: rec {
        python3 = prev.python3.override {
          self = python3;
          packageOverrides = self: super: {
            nix-prefetch-github = super.callPackage f { };
          };
        };
        nix-prefetch-github = with final.python3.pkgs;
          toPythonApplication nix-prefetch-github;
      };
      systemIndependent = { inherit overlay; };
    in systemDependent // systemIndependent;
}
