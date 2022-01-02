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
	"rev": "856d511bd65dec00bfa2bee6b68b1479699def3d",
	"sha256": "ACSWdkcCCfptbkusYiPs5j651tC62JN+W4s5gdWhEdk=",
	"fetchSubmodules": false,
	"leaveDotGit": false,
	"deepClone": false
    }

available commands
------------------

nix-prefetch-github
^^^^^^^^^^^^^^^^^^^

This command downloads the code from a github repository and puts it
into the local nix store.  It also prints the function arguments to
``fetchFromGitHub`` to the standard output.  ::

    $ nix-prefetch-github --help
    usage: nix-prefetch-github [-h] [--fetch-submodules]
			       [--no-fetch-submodules]
			       [--leave-dot-git]
			       [--no-leave-dot-git] [--deep-clone]
			       [--no-deep-clone] [--verbose] [--nix]
			       [--json] [--rev REV] [--version]
			       owner repo

    positional arguments:
      owner
      repo

    optional arguments:
      -h, --help            show this help message and exit
      --fetch-submodules
      --no-fetch-submodules
      --leave-dot-git
      --no-leave-dot-git
      --deep-clone
      --no-deep-clone
      --verbose, -v
      --nix
      --json
      --rev REV
      --version, -V

nix-prefetch-github-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This command examins the current working directory and tries to figure
out if it is part of a git repository linked to github.  If this was
successful the program prefetches the currently checked out commit
from the ``origin`` remote repository similar to the command
``nix-prefetch-github``.
::

    $ nix-prefetch-github-directory --help
    usage: nix-prefetch-github-directory [-h] [--fetch-submodules]
					 [--no-fetch-submodules]
					 [--leave-dot-git]
					 [--no-leave-dot-git]
					 [--deep-clone]
					 [--no-deep-clone]
					 [--verbose] [--nix]
					 [--json]
					 [--directory DIRECTORY]
					 [--remote REMOTE]

    optional arguments:
      -h, --help            show this help message and exit
      --fetch-submodules
      --no-fetch-submodules
      --leave-dot-git
      --no-leave-dot-git
      --deep-clone
      --no-deep-clone
      --verbose, -v
      --nix
      --json
      --directory DIRECTORY
      --remote REMOTE

nix-prefetch-github-latest-release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This command fetches the code for the latest release of the specified
repository.
::

    $ nix-prefetch-github-latest-release --help
    usage: nix-prefetch-github [-h] [--fetch-submodules]
			       [--no-fetch-submodules]
			       [--leave-dot-git]
			       [--no-leave-dot-git] [--deep-clone]
			       [--no-deep-clone] [--verbose] [--nix]
			       [--json] [--version]
			       owner repo

    positional arguments:
      owner
      repo

    optional arguments:
      -h, --help            show this help message and exit
      --fetch-submodules
      --no-fetch-submodules
      --leave-dot-git
      --no-leave-dot-git
      --deep-clone
      --no-deep-clone
      --verbose, -v
      --nix
      --json
      --version, -V

development environment
-----------------------

Use ``nix develop`` with flake support enabled.  Development without
nix flake support is not officially supported.  Run the provided tests
via ``python -m unittest discover``.  You can control what kind of
tests are run via the variable ``DISABLED_TESTS``::

  # Only run tests that don't hit network and don't use nix
  DISABLED_TESTS="network requires_nix_build" python -m unittest discover

Currently ``network`` and ``requires_nix_build`` are the only values
that make sense with this environment variable.

changes
-------

v5.0.1
^^^^^^

- Fix breaking bug in hash generation

v5.0.0
^^^^^^

- Remove all dependencies to other python packages other than "core" ones
- Allow users to control debugging output via the ``--verbosity`` cli
  option
- All commands now understand ``--fetch-submodules`` and
  ``--no-fetch-submodules`` options
- Commands now understand ``--leave-dot-git`` and
  ``--no-leave-dot-git`` options
- Commands now understand ``--deep-clone`` and ``--no-deep-clone``

v4.0.4
^^^^^^

- Print standard error output of subprocesses for better debugging

v4.0.3
^^^^^^

- Generated hashes now don't have a "sha256-" prefix
- jinja2 is no longer a dependency of nix-prefetch-github

v4.0.2
^^^^^^
- packaging release, no bugfixes or features

v4.0.1
^^^^^^

- Fix issue #38

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
