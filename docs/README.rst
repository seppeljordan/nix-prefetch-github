Introduction
============

This module implements a python function and a command line tool to help
you fetch sources from github when using ``fetchFromGitHub``.

This program can be distributed under the conditions of the GNU Public
License Version 3. Check out ``LICENSE.txt`` to read the license text.

Dependencies
============

-  Python and its standard library
-  nix-prefetch-url
-  nix-prefech-github
-  git
-  nix

Command Line Example
====================

.. code:: bash

   result/bin/nix-prefetch-github seppeljordan nix-prefetch-github

::

   {
       "owner": "seppeljordan",
       "repo": "nix-prefetch-github",
       "rev": "3147340eb140103b8c06e0aa8bd2c65a28d10502",
       "hash": "sha256-zQ7aoLrbawYRhqhcqyZimXY1jlYexSn6gtFn0Pep+b0="
   }

Available Commands
==================

.. _nix-prefetch-github-1:

nix-prefetch-github
-------------------

This command downloads the code from a github repository and puts it
into the local nix store. It also prints the function arguments to
``fetchFromGitHub`` to the standard output. :

::

   usage: nix-prefetch-github [-h] [--fetch-submodules] [--no-fetch-submodules]
                  [--leave-dot-git] [--no-leave-dot-git]
                  [--deep-clone] [--no-deep-clone] [--verbose]
                  [--quiet] [--nix] [--json] [--meta] [--version]
                  [--rev REV]
                  owner repo

   positional arguments:
     owner
     repo

   options:
     -h, --help            show this help message and exit
     --fetch-submodules    Include git submodules in the output derivation
     --no-fetch-submodules
               Don't include git submodules in output derivation
     --leave-dot-git       Include .git folder in output derivation. Use this if
               you need repository data, e.g. current commit hash,
               for the build process.
     --no-leave-dot-git    Don't include .git folder in output derivation.
     --deep-clone          Include all of the repository history in the output
               derivation. This option implies --leave-dot-git.
     --no-deep-clone       Don't include the repository history in the output
               derivation.
     --verbose, -v         Print additional information about the programs
               execution. This is useful if you want to issue a bug
               report.
     --quiet, -q           Print less information about the programs execution.
     --nix                 Output the results as valid nix code.
     --json                Output the results in the JSON format
     --meta                Output the results in JSON format where the arguments
               to fetchFromGitHub are located under the src key of
               the resulting json dictionary and meta information
               about the prefetched repository is located under the
               meta key of the output.
     --version             show program's version number and exit
     --rev REV

nix-prefetch-github-directory
-----------------------------

This command examins the current working directory and tries to figure
out if it is part of a git repository linked to github. If this was
successful the program prefetches the currently checked out commit from
the ``origin`` remote repository similar to the command
``nix-prefetch-github``.

::

   usage: .nix-prefetch-github-directory-wrapped [-h] [--fetch-submodules]
                         [--no-fetch-submodules]
                         [--leave-dot-git]
                         [--no-leave-dot-git]
                         [--deep-clone] [--no-deep-clone]
                         [--verbose] [--quiet] [--nix]
                         [--json] [--meta] [--version]
                         [--directory DIRECTORY]
                         [--remote REMOTE]

   options:
     -h, --help            show this help message and exit
     --fetch-submodules    Include git submodules in the output derivation
     --no-fetch-submodules
               Don't include git submodules in output derivation
     --leave-dot-git       Include .git folder in output derivation. Use this if
               you need repository data, e.g. current commit hash,
               for the build process.
     --no-leave-dot-git    Don't include .git folder in output derivation.
     --deep-clone          Include all of the repository history in the output
               derivation. This option implies --leave-dot-git.
     --no-deep-clone       Don't include the repository history in the output
               derivation.
     --verbose, -v         Print additional information about the programs
               execution. This is useful if you want to issue a bug
               report.
     --quiet, -q           Print less information about the programs execution.
     --nix                 Output the results as valid nix code.
     --json                Output the results in the JSON format
     --meta                Output the results in JSON format where the arguments
               to fetchFromGitHub are located under the src key of
               the resulting json dictionary and meta information
               about the prefetched repository is located under the
               meta key of the output.
     --version             show program's version number and exit
     --directory DIRECTORY
     --remote REMOTE

nix-prefetch-github-latest-release
----------------------------------

This command fetches the code for the latest release of the specified
repository.

::

   usage: nix-prefetch-github-latest-release [-h] [--fetch-submodules]
                         [--no-fetch-submodules]
                         [--leave-dot-git]
                         [--no-leave-dot-git] [--deep-clone]
                         [--no-deep-clone] [--verbose]
                         [--quiet] [--nix] [--json] [--meta]
                         [--version]
                         owner repo

   positional arguments:
     owner
     repo

   options:
     -h, --help            show this help message and exit
     --fetch-submodules    Include git submodules in the output derivation
     --no-fetch-submodules
               Don't include git submodules in output derivation
     --leave-dot-git       Include .git folder in output derivation. Use this if
               you need repository data, e.g. current commit hash,
               for the build process.
     --no-leave-dot-git    Don't include .git folder in output derivation.
     --deep-clone          Include all of the repository history in the output
               derivation. This option implies --leave-dot-git.
     --no-deep-clone       Don't include the repository history in the output
               derivation.
     --verbose, -v         Print additional information about the programs
               execution. This is useful if you want to issue a bug
               report.
     --quiet, -q           Print less information about the programs execution.
     --nix                 Output the results as valid nix code.
     --json                Output the results in the JSON format
     --meta                Output the results in JSON format where the arguments
               to fetchFromGitHub are located under the src key of
               the resulting json dictionary and meta information
               about the prefetched repository is located under the
               meta key of the output.
     --version             show program's version number and exit

development environment
=======================

Use ``nix develop`` with flake support enabled. Development without nix
flake support is not officially supported. Run the provided tests via
``pytest``. You can control what kind of tests are run via the variable
``DISABLED_TESTS``:

::

   # Only run tests that don't hit network and don't use nix
   DISABLED_TESTS="network requires_nix_build" pytest

Currently ``network`` and ``requires_nix_build`` are the only values
that make sense with this environment variable.

You can visualize the dependency graph of the individual python modules
via the ``./generate-dependency-graph`` program.

You can generate a coverage report for the tests via

::

   coverage run -m nix_prefetch_github.run_tests && coverage html

changes
=======

v8.0.0 (not released yet)
-------------------------

-  Drop official support for Python versions <3.11 and introduce
   official support for Python version 3.12
-  Drop nix-build based prefetcher. This means that users need to have
   ``nix-prefetch-git`` and ``nix-prefetch=url`` available in their
   PATH.

v7.1.0
------

-  Add ``-q`` / ``--quiet`` option to decrease logging verbosity
-  Add ``--meta`` option to include the commit timestamp of the latest
   prefetched commit in the output
-  Use content of ``=GITHUB_TOKEN=`` environment variable for
   authenticating with GitHub API

v7.0.0
------

-  The output format changed. In previous versions the json and nix
   output included ``sha256`` as a field. This field was removed in
   favour of a ``hash`` field. The value of this field is an SRI hash.

v6.0.1
------

-  Fix bug in repository detection for ``nix-prefetch-github-directory``

v6.0.0
------

-  Drop support for python3.8
-  Drop default arguments to fetchFromGitHub from json output (e.g.
   ``leaveDotGit = false;``, ``fetchSubmodule = false;``,
   ``deepClone = false;``)

v5.2.2
------

-  Add more info to error messages

v5.2.1
------

-  Fixed a bug that broke the program for users without the experimental
   \`nix-command\` feature

v5.2.0
------

-  Emit warning if unsafe options –deep-clone and –leave-dot-git are
   used.
-  Improve –help output slightly
-  Declutter verbose logging output

v5.1.2
------

-  Use old prefetch implementation because of bug in
   ``nix-prefetch-git``. See `this github
   issue <https://github.com/NixOS/nixpkgs/issues/168147>`__

v5.1.1
------

-  Fix bug that broke ``nix-prefetch-github --version``

v5.1.0
------

-  Use ``nix-prefetch-git`` and ``nix-prefetch-url`` for calculating
   sha256 sums when possible. The application will fall back to the old
   method when ``nix-prefetch-*`` are not available.

v5.0.1
------

-  Fix breaking bug in hash generation

v5.0.0
------

-  Remove all dependencies to other python packages other than "core"
   ones
-  Allow users to control debugging output via the ``--verbosity`` cli
   option
-  All commands now understand ``--fetch-submodules`` and
   ``--no-fetch-submodules`` options
-  Commands now understand ``--leave-dot-git`` and
   ``--no-leave-dot-git`` options
-  Commands now understand ``--deep-clone`` and ``--no-deep-clone``

v4.0.4
------

-  Print standard error output of subprocesses for better debugging

v4.0.3
------

-  Generated hashes now don't have a "sha256-" prefix
-  jinja2 is no longer a dependency of nix-prefetch-github

v4.0.2
------

-  packaging release, no bugfixes or features

v4.0.1
------

-  Fix issue #38

v4.0
----

-  Make fetching submodules the default in calls to python routines. The
   CLI should be uneffected by this change.
-  Remove default values for ``fetch_submodules`` in all internal
   classes.
-  Implement ``nix-prefetch-github-latest-release`` command

v3.0
----

-  major changes to the internal module structure
-  introduction of the ``nix-prefetch-github-directory`` command
-  code repository now functions as a nix flake

v2.4
----

-  added ``--fetch-submodules`` flag
-  Fixed incompability with nix 2.4

v2.3.2
------

-  fix issues #21, #22
-  nix-prefetch-github now accepts full ref names, e.g.
   ``refs/heads/master`` which was broken since 2.3 (#23)

v2.3.1
------

-  Fix bug in generated nix expression
-  Fix bug that prevented targeting tags with prefetch command
-  Improve error message format in case revision is not found

v2.3
----

-  Remove dependency to ``requests``
-  Default to ``master`` branch instead of first branch in list

v2.2
----

-  Add ``--version`` flag
-  Fix bug in output formatting

v2.1
----

-  Fix bug (#4) that made ``nix-prefetch-github`` incompatible with
   ``nix 2.2``.

v2.0
----

-  The result of nix\ :sub:`pretchgithub` and its corresponding command
   line tool now contains always the actual commit hash as detected by
   the tool instead of the branch or tag name.
-  Add a new flag ``--nix`` that makes the command line tool output a
   valid nix expression
-  Removed the ``--hash-only`` and ``--no-hash-only`` flags and changed
   add ``--prefetch`` and ``--no-prefetch`` flags to replace them.
