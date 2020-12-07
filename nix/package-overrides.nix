self: super: {
  pydeps = self.callPackage ./pydeps.nix { };
  stdlib-list = self.callPackage ./stdlib-list.nix { };
  nix-prefetch-github = self.callPackage ./nix-prefetch-github.nix { };
}
