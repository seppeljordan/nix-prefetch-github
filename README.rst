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

    this derivation will be built:
      /nix/store/81pc9rhpfw47khbf5g6s8frf3c9idndr-source.drv
    building '/nix/store/81pc9rhpfw47khbf5g6s8frf3c9idndr-source.drv'...
    exporting https://github.com/seppeljordan/nix-prefetch-github.git (rev ac1135c6e442aa738012bf03acad1406e2c33813) into /nix/store/sjmd6h045cp416pmfbxr1idsidcd7bl0-source
    Initialized empty Git repository in /nix/store/sjmd6h045cp416pmfbxr1idsidcd7bl0-source/.git/
    remote: Enumerating objects: 77, done.
    remote: Counting objects: 100% (77/77), done.
    remote: Compressing objects: 100% (71/71), done.
    remote: Total 77 (delta 1), reused 42 (delta 0), pack-reused 0
    Unpacking objects: 100% (77/77), 92.42 KiB | 610.00 KiB/s, done.
    From https://github.com/seppeljordan/nix-prefetch-github
     * branch            HEAD       -> FETCH_HEAD
    Switched to a new branch 'fetchgit'
    removing `.git'...
    error: hash mismatch in fixed-output derivation '/nix/store/81pc9rhpfw47khbf5g6s8frf3c9idndr-source.drv':
	     specified: sha256-u42evoAl/P3/Ad6lcXgS1+dd2fcBwEqu4gNU/OjxlPg=
		got:    sha256-UaNZNLcjBVx2FVSBNHW8pIle+77QZAze801vjbiJHEI=

    /nix/store/r4s5kri1ppqbvkpfm7gcv38x8dvsf0x3-source

    {
	"owner": "seppeljordan",
	"repo": "nix-prefetch-github",
	"rev": "ac1135c6e442aa738012bf03acad1406e2c33813",
	"sha256": "UaNZNLcjBVx2FVSBNHW8pIle+77QZAze801vjbiJHEI=",
	"fetchSubmodules": true
    }

python example
--------------

::

    $ python
    Python 3.8.9 (default, Apr  2 2021, 11:20:07)
    [GCC 10.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import nix_prefetch_github
    >>> nix_prefetch_github.nix_prefetch_github(owner="seppeljordan", repo="nix-prefetch-github")

    this derivation will be built:
      /nix/store/rd1aliq59rb580pfyz05h43kj87s09yp-source.drv
    building '/nix/store/rd1aliq59rb580pfyz05h43kj87s09yp-source.drv'...

    trying https://github.com/seppeljordan/nix-prefetch-github/archive/ac1135c6e442aa738012bf03acad1406e2c33813.tar.gz
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
				     Dload  Upload   Total   Spent    Left  Speed
    100   174  100   174    0     0    646      0 --:--:-- --:--:-- --:--:--   646
    100 88107    0 88107    0     0   149k      0 --:--:-- --:--:-- --:--:--  149k
    unpacking source archive /build/ac1135c6e442aa738012bf03acad1406e2c33813.tar.gz
    error: hash mismatch in fixed-output derivation '/nix/store/rd1aliq59rb580pfyz05h43kj87s09yp-source.drv':
	     specified: sha256-u42evoAl/P3/Ad6lcXgS1+dd2fcBwEqu4gNU/OjxlPg=
		got:    sha256-UaNZNLcjBVx2FVSBNHW8pIle+77QZAze801vjbiJHEI=

    /nix/store/r4s5kri1ppqbvkpfm7gcv38x8dvsf0x3-source

    PrefetchedRepository(repository=GithubRepository(owner='seppeljordan', name='nix-prefetch-github'), rev='ac1135c6e442aa738012bf03acad1406e2c33813', sha256='UaNZNLcjBVx2FVSBNHW8pIle+77QZAze801vjbiJHEI=', fetch_submodules=False)


available commands
------------------

nix-prefetch-github
^^^^^^^^^^^^^^^^^^^

This command downloads the code from a github repository and puts it
into the local nix store.  It also prints the function arguments to
``fetchFromGitHub`` to the standard output.  ::

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

v5.0.0
^^^^^^

- Remove all dependencies to other python packages other than "core" ones
- Allow users to control debugging output via the ``--verbosity`` cli
  option
- All commands now understand ``--fetch-submodules`` and
  ``--no-fetch-submodules`` options

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
