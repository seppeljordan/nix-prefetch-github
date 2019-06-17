from setuptools import setup

setup(
    url='https://github.com/seppeljordan/nix-prefetch-github',
    data_files=[
        ('templates', [
            'src/nix_prefetch_github/templates/prefetch-github.nix.j2',
            'src/nix_prefetch_github/templates/nix-output.j2',
            'src/nix_prefetch_github/VERSION',
        ])
    ],
    include_package_data=True,
)
