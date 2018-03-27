from distutils.core import setup

with open('VERSION') as f:
    version = f.readlines()[0]

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='nix-prefetch-github',
    description='Prefetch source code from github for nix build tool',
    long_description=long_description,
    version=version,
    package_dir={'': 'src'},
    install_requires=[
        'attrs',
        'click',
        'effect',
        'jinja2',
        'requests',
    ],
    packages=[
        'nix_prefetch_github'
    ],
    entry_points={
        'console_scripts': [
            'nix-prefetch-github = nix_prefetch_github:_main'
        ]
    },
    data_files=[
        ('templates', ['src/nix_prefetch_github/templates/prefetch-github.nix.j2'])
    ],
    include_package_data=True,
)
