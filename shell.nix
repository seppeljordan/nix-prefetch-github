let
  nixpkgs = import <nixpkgs> {};
  interpreter =
    (import ./requirements.nix { pkgs = nixpkgs; })
    .interpreter;
in
  with nixpkgs;
  stdenv.mkDerivation {
    name = "env";
    src = ./.;
    buildInputs = [
      interpreter
      nix-prefetch-scripts
    ];
  }
