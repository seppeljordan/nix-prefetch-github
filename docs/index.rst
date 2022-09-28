Welcome to nix-prefetch-github's documentation!
===============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Available programs
==================

nix-prefetch-github
-------------------

.. argparse::
   :module: nix_prefetch_github.controller.nix_prefetch_github_controller
   :func: get_argument_parser
   :prog: nix-prefetch-github

   Use this program to generate the arguments for ``fetchFromGitHub``
   nix function.

nix-prefetch-github-directory
-----------------------------

.. argparse::
   :module: nix_prefetch_github.controller.nix_prefetch_github_directory_controller
   :func: get_argument_parser
   :prog: nix-prefetch-github-directory

   Use this program to generate a nix expression for
   ``fetchFromGitHub`` based on the git repository in the local
   directory.

nix-prefetch-latest-release
---------------------------

.. argparse::
   :module: nix_prefetch_github.controller.nix_prefetch_github_latest_release_controller
   :func: get_argument_parser
   :prog: nix-prefetch-github-latest-release

   Use this program to generate a nix expression for the latest
   release of a github repository.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
