#!/usr/bin/env sh

set -e

VERSION=$(cat nix_prefetch_github/VERSION)

./clean
./test-prefetch
./clean
git tag "v${VERSION}"
python setup.py sdist
twine upload "dist/nix-prefetch-github-${VERSION}.tar.gz"
git push origin "v${VERSION}"
