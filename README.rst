nix-prefetch-github
===================

This module implements a python function and a command line tool to
help you fetch sources from github when using ``fetchFromGitHub``.

This program can be distributed under the conditions of the GNU Public
License Version 3.  Check out ``LICENSE.txt`` to read the license
text.

command line example
--------------------

::

    $ nix-prefetch-github seppeljordan nix-prefetch-github
    {
        "owner": "seppeljordan",
        "repo": "nix-prefetch-github",
        "rev": "603f42203db128a7aaa091cf34d406bf7a80e9f0",
        "sha256": "1wrvvy85x7yqj4rkgpj93cdnhalyhzpr8pmyca38v59lm5ndh2w4"
    }

python example
--------------

::

    Python 3.6.4 (default, Dec 19 2017, 05:36:13)
    [GCC 7.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import nix_prefetch_github
    >>> nix_prefetch_github.nix_prefetch_github(owner="seppeljordan", repo="nix-prefetch-github")
    {'owner': 'seppeljordan', 'repo': 'nix-prefetch-github', 'rev': '603f42203db128a7aaa091cf34d406bf7a80e9f0', 'sha256': '1wrvvy85x7yqj4rkgpj93cdnhalyhzpr8pmyca38v59lm5ndh2w4'}


available commands
------------------

nix-prefetch-github
^^^^^^^^^^^^^^^^^^^

This command downloads the code from a github repository and puts it
into the local nix store.  It also prints the command line arguments
for downloading to the standard output.
::

   $ nix-prefetch-github --help
   Usage: nix-prefetch-github [OPTIONS] OWNER REPO

   Options:
     --prefetch / --no-prefetch  Prefetch given repository into nix store
     --nix                       Format output as Nix expression
     --fetch-submodules          Whether to fetch submodules contained in the
				 target repository

     --rev TEXT
     --version                   Show the version and exit.
     --help                      Show this message and exit.


nix-prefetch-github-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This command examins the current working directory and tries to figure
out if it is part of a git repository linked to github.  If this was
successful the program prefetches the currently checked out commit
from the ``origin`` remote repository similar to the command
``nix-prefetch-github``.
::

    $ nix-prefetch-github-directory --help
    Usage: nix-prefetch-github-directory [OPTIONS]

    Options:
      --directory TEXT
      --nix                       Format output as Nix expression
      --prefetch / --no-prefetch  Prefetch given repository into nix store
      --remote TEXT
      --fetch-submodules          Whether to fetch submodules contained in the
				  target repository

      --help                      Show this message and exit.



nix-prefetch-github-latest-release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This command fetches the code for the latest release of the specified
repository.
::

    $ nix-prefetch-github-latest-release --help
    Usage: nix-prefetch-github-latest-release [OPTIONS] OWNER REPO

    Options:
      --nix                       Format output as Nix expression
      --prefetch / --no-prefetch  Prefetch given repository into nix store
      --fetch-submodules          Whether to fetch submodules contained in the
				  target repository

      --help                      Show this message and exit.

   

changes
-------

v4.0
^^^^

- Make fetching submodules the default in calls to python routines.
  The CLI should be uneffected by this change.
- Remove default values for ``fetch_submodules`` in all internal
  classes.
- Implement ``nix-prefetch-github-latest-release`` command

v3.0
^^^^

- major changes to the internal module structure
- introduction of the ``nix-prefetch-github-directory`` command
- code repository now functions as a nix flake

v2.4
^^^^

- added ``--fetch-submodules`` flag
- Fixed incompability with nix 2.4

v2.3.2
^^^^^^

- fix issues #21, #22
- nix-prefetch-github now accepts full ref names,
  e.g. ``refs/heads/master`` which was broken since 2.3 (#23)

v2.3.1
^^^^^^

- Fix bug in generated nix expression
- Fix bug that prevented targeting tags with prefetch command
- Improve error message format in case revision is not found

v2.3
^^^^

- Remove dependency to ``requests``
- Default to ``master`` branch instead of first branch in list

v2.2
^^^^

- Add ``--version`` flag
- Fix bug in output formatting

v2.1
^^^^

- Fix bug (#4) that made ``nix-prefetch-github`` incompatible with
  ``nix 2.2``.

v2.0
^^^^

- The result of nix_pretch_github and its corresponding command line
  tool now contains always the actual commit hash as detected by the
  tool instead of the branch or tag name.
- Add a new flag ``--nix`` that makes the command line tool output a
  valid nix expression
- Removed the ``--hash-only`` and ``--no-hash-only`` flags and changed
  add ``--prefetch`` and ``--no-prefetch`` flags to replace them.
