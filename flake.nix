{
  description = "nix-prefetch-github";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    nixpkgs-stable.url = "github:NixOS/nixpkgs/nixos-23.11";
  };

  outputs = { self, nixpkgs, flake-utils, nixpkgs-stable, ... }:
    let
      systemDependent = flake-utils.lib.eachSystem supportedSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ self.overlays.default ];
          };
          pkgsStable = import nixpkgs-stable {
            inherit system;
            overlays = [ self.overlays.default ];
          };
          python = pkgs.python3;
        in {
          packages = { default = pkgs.nix-prefetch-github; };
          devShells = {
            default = pkgs.callPackage nix/dev-shell.nix { };
            stable = pkgsStable.callPackage nix/dev-shell.nix { };
          };
          checks = {
            defaultPackage = self.packages.${system}.default;
            nixosStablePackage = pkgsStable.nix-prefetch-github;
            nix-prefetch-github-python39 =
              pkgs.python39.pkgs.nix-prefetch-github;
            nix-prefetch-github-python310 =
              pkgs.python310.pkgs.nix-prefetch-github;
            nix-prefetch-github-python311 =
              pkgs.python311.pkgs.nix-prefetch-github;
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
                  . \
                  test-pypi-install
              mkdir $out
            '';
            flake8-check = pkgs.runCommand "flake8-nix-prefetch-github" { } ''
              cd ${self}
              ${python.pkgs.flake8}/bin/flake8
              mkdir $out
            '';
            nixfmt-check = pkgs.runCommand "nixfmt-nix-prefetch-github" { } ''
              ${pkgs.nixfmt}/bin/nixfmt --check \
                $(find ${self} -type f -name '*.nix')
              mkdir $out
            '';
          };
        });
      systemIndependent = {
        overlays.default = final: prev: {
          pythonPackagesExtensions = prev.pythonPackagesExtensions
            ++ [ (import nix/package-overrides.nix) ];
        };
      };
      supportedSystems = flake-utils.lib.defaultSystems;
    in systemDependent // systemIndependent;
}
