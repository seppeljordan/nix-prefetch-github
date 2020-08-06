import os.path

import jinja2

HERE = os.path.dirname(__file__)
templates_env = jinja2.Environment(loader=jinja2.FileSystemLoader(HERE + "/templates"))
template = templates_env.get_template("prefetch-github.nix.j2")
output_template = templates_env.get_template("nix-output.j2")
