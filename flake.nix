{
  description = "nix-prefetch-github";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    let
      systemDependent = flake-utils.lib.eachSystem supportedSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ self.overlays.default ];
          };
          python = pkgs.python3;
        in {
          packages = {
            default = with python.pkgs; toPythonApplication nix-prefetch-github;
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
            nix-prefetch-github-python38 =
              pkgs.python38.pkgs.nix-prefetch-github;
            nix-prefetch-github-python39 =
              pkgs.python39.pkgs.nix-prefetch-github;
            nix-prefetch-github-python310 =
              pkgs.python310.pkgs.nix-prefetch-github;
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
          python38 =
            overridePython prev.python38 (import nix/package-overrides.nix);
          python39 =
            overridePython prev.python39 (import nix/package-overrides.nix);
          python310 =
            overridePython prev.python310 (import nix/package-overrides.nix);
          python311 =
            overridePython prev.python311 (import nix/package-overrides.nix);
          nix-prefetch-github = with final.python3.pkgs;
            toPythonApplication nix-prefetch-github;
        };
      };
      overridePython = pythonSelf: overrides:
        pythonSelf // {
          pkgs = pythonSelf.pkgs.overrideScope overrides;
        };
      supportedSystems = flake-utils.lib.defaultSystems;
    in systemDependent // systemIndependent;
}
