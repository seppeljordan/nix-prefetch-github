let
  nixpkgs = import <nixpkgs> { };
  pythonPackages = import ./requirements.nix { pkgs = nixpkgs; };

in nixpkgs.mkShell {
  buildInputs = [ pythonPackages.interpreter ];
  shellHook = ''
    export PYTHONPATH=${./src}:$PYTHONPATH
  '';
}
