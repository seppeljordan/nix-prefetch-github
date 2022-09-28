import sys
from typing import List

from nix_prefetch_github.version import VERSION_STRING

sys.path.append("..")
project = "nix-prefetch-github"
copyright = "2022, Sebastian Jordan"
author = "Sebastian Jordan"
release = VERSION_STRING
extensions = ["sphinxarg.ext"]
templates_path = ["_templates"]
exclude_patterns: List[str] = []
html_theme = "alabaster"
html_static_path = ["_static"]
