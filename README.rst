nix-prefetch-github
===================

This module implements a python function and a command line tool to
help you fetch sources from github when using ``fetchFromGitHub``.

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
