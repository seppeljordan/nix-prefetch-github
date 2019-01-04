let
  nixpkgs = import <nixpkgs> {};
  pkgs = (import ./requirements.nix { pkgs = nixpkgs; });
in
  pkgs.packages.nix-prefetch-github
