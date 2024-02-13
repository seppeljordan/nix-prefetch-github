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

Configuration
=============

Github API Token
----------------

All the commands provided by this package will read the environment
variable ``GITHUB_TOKEN`` and use its content verbatim as an
authentication/authorization token when requesting from GitHubs API.

output formats
==============

The different command line programs of this package provide different
output formats. Those can be selected via different arguments provided
to the program.

JSON output
-----------

The ``--json`` argument is the default and will render
the output as JSON to the standard output of the program. The
resulting json value will consist of a single dictionary where all key
value pairs correspond to the arguments to the ``fetchFromGitHub``
function provided by ``nixpkgs``. It is intended to be used directly in
nix code::

  src = with builtins; fetchFromGitHub (fromJSON (readFile ./nix-prefetch-github-output.json))


Meta information output
-----------------------

The ``--meta`` argument produces output similar to the output produced
by ``--json``. The difference is that a nested dictionary is produced
with two top level keys: ``src`` and ``meta``. The ``src`` key will
contain the same data as would have been yielded by ``--json`` whereas
the ``meta`` key contains some meta data on the commit that was
fetched. At the moment this will only be the date and time of day of
the latest commit. This can be useful when providing nightly versions
of a package::

  let fetchedSourceCode = (fromJSON (readFile ./nix-prefetch-github-output.json));
  in buildPackage {
    pname = "my-package";
    version = fetchedSourceCode.meta.commitDate;
    src = fetchFromGitHub fetchedSourceCode.src;
    ...
  };

Nix output
----------

Consider this a legacy output format without any practical
applications. The ``--nix`` argument will result in a valid nix
expression produced by the respective program.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
