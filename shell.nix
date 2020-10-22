let
  lock = builtins.fromJSON (builtins.readFile ./flake.lock);
  system = builtins.currentSystem;
  flake-compat-source = fetchTarball {
    url =
      "https://github.com/edolstra/flake-compat/archive/${lock.nodes.flake-compat.locked.rev}.tar.gz";
    sha256 = lock.nodes.flake-compat.locked.narHash;
  };
  flake-compat = import flake-compat-source;
  nix-prefetch-github = (flake-compat { src = ./.; }).shellNix.packages."${system}".python.pkgs.nix-prefetch-github;
  maybeAttrs = attributeSet: name: default:
    if builtins.hasAttr name attributeSet then
      attributeSet."${name}"
    else
      default;
  debug = with builtins;
    trace "${concatStringsSep " " (attrNames nix-prefetch-github)}";
in debug (nix-prefetch-github.overridePythonAttrs (old: {
  nativeBuildInputs = maybeAttrs old "nativeBuildInputs" [ ]
    ++ maybeAttrs old "checkInputs" [ ];
}))
