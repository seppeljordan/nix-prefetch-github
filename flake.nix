{
  description = "nix-prefetch-github";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
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
        in rec {
          defaultPackage = with python.pkgs;
            toPythonApplication nix-prefetch-github;
          packages = { inherit python; };
          checks = {
            inherit defaultPackage;
            nixfmt-check = pkgs.runCommand "nixfmt-nix-prefetch-github" { } ''
              ${pkgs.nixfmt}/bin/nixfmt --check \
                $(find ${self} -type f -name '*.nix')
              mkdir $out
            '';
            black-check = pkgs.runCommand "black-nix-prefetch-github" { } ''
              cd ${self}
              ${python.pkgs.black}/bin/black --check .
              mkdir $out
            '';
            mypy-check = pkgs.runCommand "mypy-nix-prefetch-github" { } ''
              cd ${self}
              ${python.pkgs.mypy}/bin/mypy nix_prefetch_github tests
              mkdir $out
            '';
            isort-check = pkgs.runCommand "isort-nix-prefetch-github" { } ''
              cd ${self}
              ${python.pkgs.isort}/bin/isort \
                  --settings-path setup.cfg \
                  --check-only \
                  -df \
                  -rc \
                  .
              mkdir $out
            '';
            flake8-check = pkgs.runCommand "flake8-nix-prefetch-github" { } ''
              cd ${self}
              ${python.pkgs.flake8}/bin/flake8
              mkdir $out
            '';
          };
        });
      systemIndependent = { inherit overlay; };
    in systemDependent // systemIndependent;
}
