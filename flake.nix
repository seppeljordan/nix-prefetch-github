{
  description = "nix-prefetch-github";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    let
      # pyopenssl does not build on aarch64-darwin
      supportedSystems = builtins.filter (s: s != "aarch64-darwin")
        flake-utils.lib.defaultSystems;
      systemDependent = flake-utils.lib.eachSystem supportedSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ self.overlays.default ];
          };
          python = pkgs.python3;
        in {
          packages = {
            inherit python;
            default = with python.pkgs; toPythonApplication nix-prefetch-github;
            nix-prefetch-github = self.packages."${system}".default;
          };
          devShells.default = pkgs.mkShell {
            packages = (with pkgs; [ git nixfmt nix-prefetch-scripts pandoc ])
              ++ (with python.pkgs; [
                black
                flake8
                mypy
                twine
                virtualenv
                isort
                coverage
                pydeps
              ]);
            inputsFrom = [ python.pkgs.nix-prefetch-github ];
          };
          checks = {
            defaultPackage = self.packages.${system}.default;
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
          python3 = prev.python3.override {
            packageOverrides = import nix/package-overrides.nix;
          };
          nix-prefetch-github = with final.python3.pkgs;
            toPythonApplication nix-prefetch-github;
        };
      };
    in systemDependent // systemIndependent;
}
