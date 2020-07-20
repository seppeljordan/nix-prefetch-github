{
  description = "nix-prefetch-github";

  inputs = { nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.03"; };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "i686-linux" "x86_64-darwin" "aarch64-linux" ];
      lib = nixpkgs.lib;
      forAllSystems = f: lib.genAttrs systems (system: f system);
      version = builtins.readFile nix_prefetch_github/VERSION;
      f = { buildPythonApplication, attrs, click, effect, jinja2 }:
        buildPythonApplication {
          pname = "nix-prefetch-github";
          version = version;
          src = ./.;
          propagatedBuildInputs = [ attrs click effect jinja2 ];
          doCheck = false;
        };
    in {
      defaultPackage = forAllSystems (system:
        nixpkgs.outputs.legacyPackages."${system}".python3.pkgs.callPackage f
        { });
      function = f;
    };
}
