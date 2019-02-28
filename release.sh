#!/usr/bin/env sh

set -e

VERSION=$(cat src/nix_prefetch_github/VERSION)

./clean
./test-prefetch
./clean
git tag "v${VERSION}"
nix-shell --command 'exec python setup.py sdist'
nix-shell -p python3Packages.twine \
          --command "twine upload dist/nix-prefetch-github-${VERSION}.tar.gz"
