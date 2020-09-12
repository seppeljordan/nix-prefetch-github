self: super: {
  pydeps = super.callPackage ./pydeps.nix { };
  stdlib-list = super.callPackage ./stdlib-list.nix { };
  nix-prefetch-github = super.callPackage ./nix-prefetch-github.nix { };
}
