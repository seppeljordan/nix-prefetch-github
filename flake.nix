{
  description = "nix-prefetch-github";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    let
      packageOverrides = import nix/package-overrides.nix;
      overlay = final: prev: {
        python3 = prev.python3.override { inherit packageOverrides; };
        nix-prefetch-github = with final.python3.pkgs;
          toPythonApplication nix-prefetch-github;
      };
      systemDependent = flake-utils.lib.eachDefaultSystem (system:
        let
          pkgs = nixpkgs.outputs.legacyPackages."${system}";
          python = pkgs.python3.override { inherit packageOverrides; };
        in {
          defaultPackage = with python.pkgs;
            toPythonApplication nix-prefetch-github;
        });
      systemIndependent = { inherit overlay; };
    in systemDependent // systemIndependent;
}
