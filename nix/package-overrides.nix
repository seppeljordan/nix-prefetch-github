self: super: {
  nix-prefetch-github = self.callPackage ./nix-prefetch-github.nix { };
}
