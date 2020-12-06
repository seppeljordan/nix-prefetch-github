#!/usr/bin/env sh

set -e

VERSION=$(cat nix_prefetch_github/VERSION)

python setup.py sdist
twine upload "dist/nix-prefetch-github-${VERSION}.tar.gz"
git tag "v${VERSION}"
git push origin "v${VERSION}"
