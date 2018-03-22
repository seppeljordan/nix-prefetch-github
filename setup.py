from distutils.core import setup

setup(
    name='nix-prefetch-github',
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
    include_package_data=True,
)
