{
  description = "nix-prefetch-github";

  inputs = { flake-utils.url = "github:numtide/flake-utils"; };

  outputs = { self, nixpkgs, flake-utils, ... }:
    let
      systemDependent = flake-utils.lib.eachDefaultSystem (system:
        let
          isDarwinAarch = system == "aarch64-darwin";
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ self.overlay ];
          };
          python = pkgs.python3;
          pythonEnvironment = python.withPackages (pythonPackages:
            with pythonPackages.nix-prefetch-github;
            with pythonPackages;
            buildInputs ++ propagatedBuildInputs ++ nativeBuildInputs
            ++ [ black flake8 mypy twine virtualenv isort ]);
        in {
          defaultPackage = with python.pkgs;
            toPythonApplication nix-prefetch-github;
          packages = {
            inherit python;
            nix-prefetch-github = self.defaultPackage."${system}";
          };
          devShell = pkgs.mkShell {
            name = "dev-shell";
            buildInputs = with pkgs;
              [
                git
                pythonEnvironment
              ]
              # nix code formatting on aarch64-darwin is not available
              # since ghc is broken on that system.
              ++ (nixpkgs.lib.optional (!isDarwinAarch) nixfmt);
          };
          checks = {
            defaultPackage = self.defaultPackage.${system};
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
                  . \
                  test-pypi-install
              mkdir $out
            '';
            flake8-check = pkgs.runCommand "flake8-nix-prefetch-github" { } ''
              cd ${self}
              ${python.pkgs.flake8}/bin/flake8
              mkdir $out
            '';
          } // nixpkgs.lib.optionalAttrs (!isDarwinAarch) {
            # Unfortunately ghc is broken on aarch64-darwin.  We
            # ignore the nix formatting check since it is less
            # important that formatting is checked on every possible
            # system then that the program runs.
            nixfmt-check = pkgs.runCommand "nixfmt-nix-prefetch-github" { } ''
              ${pkgs.nixfmt}/bin/nixfmt --check \
                $(find ${self} -type f -name '*.nix')
              mkdir $out
            '';
          };
        });
      systemIndependent = {
        overlay = final: prev: {
          python3 = prev.python3.override {
            packageOverrides = import nix/package-overrides.nix;
          };
          nix-prefetch-github = with final.python3.pkgs;
            toPythonApplication nix-prefetch-github;
        };
      };
    in systemDependent // systemIndependent;
}
